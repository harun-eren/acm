import unittest
import simulation


class TestSimulation(unittest.TestCase):

    def set_up_data_scenario_1(self):
        self.L = 3
        self.test_simulation = simulation.Simulation(self.L, 1, 3, visualize_grid=False)
        self.test_simulation.x = 2
        self.test_simulation.y = 0
        self.test_simulation.w = 2
        self.test_simulation.population = [
            [[1], [2], [2]],
            [[1], [2], [1]],
            [[3], [3], [3]]
        ]

    def set_up_data_scenario_2(self):
        self.L = 5
        self.test_simulation = simulation.Simulation(self.L, 1, 20, visualize_grid=False)
        self.test_simulation.x = 2
        self.test_simulation.y = 0
        self.test_simulation.w = 0
        self.test_simulation.population = [
            [[1], [2], [2], [3], [4]],
            [[5], [6], [6], [7], [8]],
            [[9], [10], [10], [11], [12]],
            [[13], [14], [14], [15], [16]],
            [[17], [18], [18], [19], [20]]
        ]

    def set_up_data_scenario_3(self):
        self.L = 5
        self.test_simulation = simulation.Simulation(self.L, 1, 20, visualize_grid=False)
        self.test_simulation.x = 3
        self.test_simulation.y = 3
        self.test_simulation.w = 1
        self.test_simulation.population = [
            [[1], [2], [1], [2], [1]],
            [[1], [3], [6], [1], [1]],
            [[1], [1], [4], [1], [9]],
            [[8], [1], [1], [1], [16]],
            [[7], [6], [5], [1], [1]]
        ]

    def set_up_data_scenario_4(self):
        self.L = 5
        self.test_simulation = simulation.Simulation(self.L, 1, 20, visualize_grid=False)
        self.test_simulation.x = 3
        self.test_simulation.y = 4
        self.test_simulation.w = 1
        self.test_simulation.population = [
            [[1], [2], [1], [2], [1]],
            [[1], [3], [6], [1], [1]],
            [[1], [1], [4], [1], [9]],
            [[8], [1], [1], [1], [16]],
            [[7], [6], [5], [1], [1]]
        ]


    def sort_2D_list(self, unsorted_data):
        sorted_data = []
        for unsorted in unsorted_data:
            unsorted.sort()
            index = 0
            for sorted in sorted_data:
                if sorted > unsorted:
                    break
                index += 1
            sorted_data.insert(index, unsorted)
        return sorted_data

    def convert_address(self, nested_list):
        converted_data = []
        for list_ in nested_list:
            converted_list = []
            for address in list_:
                converted_list.append(address[0] * self.L + address[1])
            converted_data.append(converted_list)
        return converted_data

    def test_identify_regions_scenario_1(self):
        self.set_up_data_scenario_1()
        expected_result = [
            [0, 3],
            [1, 2, 4],
            [5],
            [6, 7],
            [8]
        ]
        regs = self.test_simulation.identify_regions()
        unsorted_test_result = self.convert_address(regs)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(expected_result, test_result)
        # print(test_result)

    def test_identify_cultures_scenario_1(self):
        self.set_up_data_scenario_1()
        expected_result = [
            [0, 3, 5],
            [1, 2, 4],
            [6, 7, 8]
        ]
        cultures = self.test_simulation.identify_cultures()
        unsorted_test_result = self.convert_address(cultures)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(test_result, expected_result)
        # print("test result: ", test_result)

    def test_identify_regions_scenario_2(self):
        self.set_up_data_scenario_2()
        expected_result = []
        for i in range(25):
            expected_result.append([i])
        regs = self.test_simulation.identify_regions()
        unsorted_test_result = self.convert_address(regs)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(expected_result, test_result)

    def test_identify_cultures_scenario_2(self):
        self.set_up_data_scenario_2()
        expected_result = [[0], [1, 2], [3], [4], [5], [6, 7], [8], [9], [10], [11, 12], [13], [14], [15], [16, 17], [18], [19], [20], [21, 22], [23], [24]]
        cultures = self.test_simulation.identify_cultures()
        unsorted_test_result = self.convert_address(cultures)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(test_result, expected_result)
        # print("test result: ", test_result)

    def test_identify_regions_scenario_3(self):
        self.set_up_data_scenario_3()
        expected_result = [
            [0, 4, 5, 8, 9, 10, 11, 13, 16, 17, 18, 23, 24],
            [1],
            [2],
            [3],
            [6],
            [7],
            [12],
            [14],
            [15],
            [19],
            [20],
            [21],
            [22]
        ]
        regs = self.test_simulation.identify_regions()
        unsorted_test_result = self.convert_address(regs)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(expected_result, test_result)

    def test_identify_cultures_scenario_3(self):
        self.set_up_data_scenario_3()
        expected_result = [
            [0, 2, 4, 5, 8, 9, 10, 11, 13, 16, 17, 18, 23, 24],
            [1, 3],
            [6],
            [7, 21],
            [12],
            [14],
            [15],
            [19],
            [20],
            [22]
        ]
        cultures = self.test_simulation.identify_cultures()
        unsorted_test_result = self.convert_address(cultures)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(test_result, expected_result)
        # print("test result: ", test_result)

    def test_identify_regions_scenario_4(self):
        self.set_up_data_scenario_4()
        expected_result = [
            [0, 5, 10, 11, 16, 17],
            [1],
            [2],
            [3],
            [4, 8, 9, 13, 18, 23, 24],
            [6],
            [7],
            [12],
            [14],
            [15],
            [19],
            [20],
            [21],
            [22]
        ]
        regs = self.test_simulation.identify_regions()
        unsorted_test_result = self.convert_address(regs)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(expected_result, test_result)
        # print("test result 4: ", test_result)
        # print("expected result 4: ", expected_result)


    def test_identify_cultures_scenario_4(self):
        self.set_up_data_scenario_4()
        expected_result = [
            [0, 2, 4, 5, 8, 9, 10, 11, 13, 16, 17, 18, 23, 24],
            [1, 3],
            [6],
            [7, 21],
            [12],
            [14],
            [15],
            [19],
            [20],
            [22]
        ]
        cultures = self.test_simulation.identify_cultures()
        unsorted_test_result = self.convert_address(cultures)
        test_result = self.sort_2D_list(unsorted_test_result)
        self.assertEqual(test_result, expected_result)
        # print("test result: ", test_result)


if __name__ == '__main__':
    unittest.main()
