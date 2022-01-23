from Comparators.base_comparator import BaseComparator


class CpeComparator(BaseComparator):

    def __init__(self, config):
        super().__init__(config)
        self.weights = [
            config["vendor"],
            config["product"],
            config["version"]
        ]
        self.diff_value = config["diff_value"]

    def _compare_sw_components(self, sw1, sw2):
        # Both hosts do not have this SW component
        if sw1 is None and sw2 is None:
            return 1

        # Only one of the hosts has this SW component, use predefined diff
        # value
        if sw1 is None or sw2 is None:
            return self.diff_value

        compare_result = self._compare_cpe(sw1, sw2, self.weights)

        # Zero similarity -> use configured diff value
        if compare_result == 0:
            return self.config["diff_value"]
        return compare_result

    @staticmethod
    def _compare_cpe(sw1, sw2, weights):
        """
        Compares two software components (their CPE strings) and evaluates
        similarity with list of weights for each part.
        :param sw1: First software component
        :param sw2: Second software component
        :param weights: List of weights for CPE parts
        :return: Result similarity (float in range <0,1>)
        """
        result_similarity = 0

        # Take the shorter CPE
        for i in range(min(len(sw1.cpe_list), len(sw2.cpe_list))):
            if(CpeComparator._compare_cpe_parts(sw1.cpe_list[i],
                                                sw2.cpe_list[i])):
                # Add cpe part weight to result when parts match
                result_similarity += weights[i]
            else:
                break

        return result_similarity

    @staticmethod
    def _compare_cpe_parts(part1, part2):
        """
        Compares two CPE elements. Elements are the same, if they are equal or
        one of is *.
        :param part1:
        :param part2:
        :return:
        """
        return part1 == part2 or part1 == "*" or part2 == "*"
