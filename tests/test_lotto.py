from unittest import TestCase
from classes.lotto import Barrel, BarrelPool
# from pytest import fixture, mark, param
import classes.lotto as lotto


class TestBarrel(TestCase):
    def test_init_number_int(self):
        barrel = Barrel(10)
        self.assertEqual(10, barrel.number)

    # def test_init_number_float(self):
    #     with TypeError('Бочка может быть только с целым значением'):
    #         barrel = Barrel(10.0)
    #     self.assertEqual(10.0, barrel.number)
#
    # def test_init_number_str(self):
    #     barrel = Barrel('10')
    #     self.assertEqual('10', barrel.number)


class TestBarrelPool(TestCase):
    def test_start_len(self):
        barrel_pool = BarrelPool()
        result = len(barrel_pool._pool)
        self.assertEqual(result, lotto.BARREL_POOL_SIZE)

    def test_content(self):
        barrel_pool = BarrelPool()
        result = []
        for i in range(1, lotto.BARREL_POOL_SIZE + 1):
            result.append(i)
        self.assertEqual(result, barrel_pool.pool)

    def test_get_barrel_extracted(self):
        barrel_pool = BarrelPool()
        barrel = barrel_pool.get_barrel()
        self.assertEqual(barrel_pool.extracted_barrels, [barrel.number])

    def test_get_barrel_removed(self):
        barrel_pool = BarrelPool()
        barrel = barrel_pool.get_barrel()
        result = []
        for i in range(1, lotto.BARREL_POOL_SIZE + 1):
            result.append(i)
        result.remove(barrel.number)
        self.assertEqual(barrel_pool.pool, result)
