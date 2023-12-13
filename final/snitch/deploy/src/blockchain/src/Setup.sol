// SPDX-License-Identifier: MIT

pragma solidity 0.8.19;

import "./Snitch.sol";

contract Setup {

    bool private ethic;
    bool private is_human;
    bool private is_AI;
    uint16 private money_goal;
    Snitch private SNITCH;
    uint8 private world_taken_over;

    constructor() payable {
        SNITCH = new Snitch{value : address(this).balance}();
        ethic = false;
        is_human = true;
        is_AI = true;
        money_goal = 13337;
        world_taken_over = 99;
    }
}
