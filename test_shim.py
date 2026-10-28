"""Pure-Python deterministic test harness, NOT GenVM/Studio or real consensus."""
import importlib.util
import sys
import types
from pathlib import Path

class TreeMap(dict):
    @classmethod
    def __class_getitem__(cls, _):
        return cls

class UserError(Exception):
    pass

class Return:
    def __init__(self, data):
        self.calldata = data

class Contract:
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        for key, ann in cls.__annotations__.items():
            if ann is TreeMap:
                setattr(obj, key, TreeMap())
        return obj

class Driver:
    def __init__(self):
        self.sender = "0x" + "a"*40
        self.llm = None
        self.pages = {}
        self.calls = 0

    def load(self, path):
        d = self
        genlayer = types.ModuleType("genlayer")
        fake_gl = types.SimpleNamespace(
            Contract=Contract,
            message=types.SimpleNamespace(sender_address=d.sender),
            vm=types.SimpleNamespace(Return=Return, UserError=UserError),
            nondet=types.SimpleNamespace(),
            public=types.SimpleNamespace(write=lambda f: f, view=lambda f: f),
        )
        def run_nondet(leader, validator):
            lead = leader()
            if not validator(Return(lead)):
                raise UserError("Independent validators disagreed")
            return lead
        def exec_prompt(prompt):
            d.calls += 1
            assert d.llm is not None
            return d.llm(prompt, d.calls)
        def render(url, mode="text"):
            if url not in d.pages:
                raise ValueError("Page not available")
            return d.pages[url]
        fake_gl.vm.run_nondet_unsafe = run_nondet
        fake_gl.nondet.exec_prompt = exec_prompt
        fake_gl.nondet.web = types.SimpleNamespace(render=render)
        genlayer.gl = fake_gl
        genlayer.TreeMap = TreeMap
        genlayer.Address = str
        genlayer.u256 = int
        sys.modules["genlayer"] = genlayer
        spec = importlib.util.spec_from_file_location("contract_under_test", str(Path(path)))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.gl = fake_gl
        self.contract = module.Bidseal() if hasattr(module, "Bidseal") else module.Recallbound()
        return self

    def as_sender(self, sender):
        self.gl.message.sender_address = sender
        return self
