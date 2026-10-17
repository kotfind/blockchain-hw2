// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract task5_math {
    int32 public res;

    function add(int32 lhs, int32 rhs) public {
        res = lhs + rhs;
    }

    function sub(int32 lhs, int32 rhs) public {
        res = lhs - rhs;
    }

    function mul(int32 lhs, int32 rhs) public {
        res = lhs * rhs;
    }

    function div(int32 lhs, int32 rhs) public {
        require(rhs != 0, "cannot divide by zero");
        res = lhs / rhs;
    }
}
