// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract task5_math {
    int32 public res;

    function add(int32 lhs, int32 rhs) public returns (int32) {
        res = lhs + rhs;
        return res;
    }

    function sub(int32 lhs, int32 rhs) public returns (int32) {
        res = lhs - rhs;
        return res;
    }

    function mul(int32 lhs, int32 rhs) public returns (int32) {
        res = lhs * rhs;
        return res;
    }

    function div(int32 lhs, int32 rhs) public returns (int32) {
        require(rhs != 0, "cannot divide by zero");

        res = lhs / rhs;
        return res;
    }
}
