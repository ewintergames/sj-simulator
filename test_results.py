from jump_result import JumpResult
from result import Result
from hill import Hill
from jumper import Jumper
import pytest

hill = Hill('Zakopane HS140', 125, 140, 4.2, 0.62, 6, 7.26, None)
jmp1 = JumpResult(90.3, 136.5, 0, 0.18, [18, 18.5, 18.5, 18, 18.5], hill)
jmp2 = JumpResult(89.9, 134.5, -1, 0.20, [18.5, 18.5, 19, 18.5, 18.5], hill)

def test_jump_result1():
    jmp = jmp1
    assert(jmp.total_points == 133.8)
    assert(jmp.distance_points == 80.7)
    assert(jmp.wind_points == -1.9)
    assert(jmp.gate_points == 0)
    assert(jmp.judges_total == 55)

def test_jump_result2():
    jmp = jmp2
    assert(jmp.total_points == 135.1)
    assert(jmp.distance_points == 77.1)
    assert(jmp.wind_points == -2.2)
    assert(jmp.gate_points == 4.7)
    assert(jmp.judges_total == 55.5)

def test_result():
    rk = Jumper("Ryoyu Kobayashi", "JPN", 80, 85, 95, 98)
    u = Result(rk)
    u.add_jump(jmp1)
    u.add_jump(jmp2)
    assert(u.total_points == 268.9)


def test_normal_hill():
    normal_hill = Hill(None, 90, 100, 0, 0, 0, 0, None)
    assert(normal_hill.points_k == 60)
    assert(normal_hill.points_meter == 2)

def test_large_hill():
    large_hill = Hill(None, 125, 140, 0, 0, 0, 0, None)
    assert(large_hill.points_k == 60)
    assert(large_hill.points_meter == 1.8)

def test_flying_hill():
    flying_hill = Hill(None, 200, 240, 0, 0, 0, 0, None)
    assert(flying_hill.points_k == 120)
    assert(flying_hill.points_meter == 1.2)