// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Governance {
    address public admin;
    mapping(address => bool) public voters;
    uint256 public proposalCounter;

    struct Proposal {
        uint256 id;
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(uint256 indexed id, string description);
    event VoteCast(address indexed voter, uint256 indexed proposalId, bool support);
    event ProposalExecuted(uint256 indexed proposalId);

    constructor() {
        admin = msg.sender;
    }

    /// @notice Add a new voter
    function addVoter(address voter) external {
        require(msg.sender == admin, "Only admin can add voters");
        voters[voter] = true;
    }

    /// @notice Create a new proposal
    /// @param description Description of the proposal
    function createProposal(string memory description) external {
        require(voters[msg.sender], "Only voters can create proposals");

        Proposal storage newProposal = proposals[proposalCounter++];
        newProposal.id = proposalCounter;
        newProposal.description = description;

        emit ProposalCreated(proposalCounter, description);
    }

    /// @notice Cast a vote on a proposal
    /// @param proposalId ID of the proposal
    /// @param support True if voting in favor, false otherwise
    function vote(uint256 proposalId, bool support) external {
        require(voters[msg.sender], "Only voters can vote");

        Proposal storage proposal = proposals[proposalId];
        require(!proposal.executed, "Proposal already executed");

        if (support) {
            proposal.votesFor++;
        } else {
            proposal.votesAgainst++;
        }

        emit VoteCast(msg.sender, proposalId, support);
    }

    /// @notice Execute a proposal
    /// @param proposalId ID of the proposal
    function executeProposal(uint256 proposalId) external {
        Proposal storage proposal = proposals[proposalId];
        require(proposal.votesFor > proposal.votesAgainst, "Proposal did not pass");
        require(!proposal.executed, "Proposal already executed");

        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }
}
