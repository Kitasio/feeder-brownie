// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./Feeder.sol";

contract FeederFactory {
    struct Birds {
        address[] addresses;
        uint256 len;
    }
    mapping(address => Birds) public feeders;

    function getFeeders(address _addr) public view returns (Birds memory) {
        return feeders[_addr];
    }

    function createFeeder(
        address[] memory _wallet,
        uint256[] memory _allocation,
        string memory _name
    ) public {
        Feeder feeder = new Feeder(_wallet, _allocation, _name);
        for (uint256 i = 0; i < _wallet.length; i++) {
            feeders[_wallet[i]].addresses.push(address(feeder));
            feeders[_wallet[i]].len += 1;
        }
    }
}
