// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract task6_token {

    // -------------------- Events Defs --------------------


    /// `from` sent `to` `amount` base units.
    event Transfer(address indexed from, address indexed to, uint amount);

    /// `from` allowed `to` to get `amount` base units.
    event Approval(address indexed from, address indexed to, uint amount);


    // -------------------- Constants --------------------


    /// A token name.
    string public constant name = "Nya Token";

    /// A token symbol.
    string public constant symbol = "NYA";

    /// `NyaUnit = BaseUnit * 10 ** decimals`;
    uint8 public constant decimals = 18;

    // `NyaUnit = BaseUnit * baseInNya`;
    uint public constant baseInNya = 10 ** uint(decimals);

    /// A total number of base units.
    uint256 public constant totalSupply = 100 * baseInNya;


    // -------------------- State --------------------


    /// An amount of base units on each account.
    mapping(address => uint) public balanceOf;

    /// `allowance[from][to] = amount` means `from` allows `to` to get `amount` base units.
    mapping(address => mapping(address => uint)) public allowance;


    // -------------------- Main --------------------

    constructor() {
        address to = msg.sender;

        balanceOf[to] = totalSupply;

        emit Transfer(address(0), to, totalSupply);
    }

    function transfer(address to, uint amount) public returns (bool) {
        address from = msg.sender;

        require(balanceOf[from] >= amount, "Not enough money");

        balanceOf[from] -= amount;
        balanceOf[to] += amount;

        emit Transfer(from, to, amount);

        return true;
    }

    function approve(address to, uint amount) public returns (bool) {
        address from = msg.sender;

        allowance[from][to] = amount;

        emit Approval(from, to, amount);

        return true;
    }

    function transferFrom(address from, address to, uint amount) public returns (bool) {
        address me = msg.sender;

        require(balanceOf[from] >= amount, "Not enough money");
        require(allowance[from][me] >= amount, "Transfer not allowed");

        allowance[from][me] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;

        emit Transfer(from, to, amount);
        return true;
    }
}
