import time
from collections import defaultdict

class Proposal:
    def __init__(self, proposal_id, creator, description):
        self.proposal_id = proposal_id
        self.creator = creator
        self.description = description
        self.votes = defaultdict(int)  # Dictionary to hold votes for each option
        self.created_at = time.time()
        self.voting_period = 86400  # Voting period in seconds (e.g., 1 day)
        self.is_active = True

    def vote(self, voter, option):
        if not self.is_active:
            raise Exception("Voting period has ended.")
        if option not in self.votes:
            self.votes[option] = 0
        self.votes[option] += 1

    def end_voting(self):
        self.is_active = False

    def get_results(self):
        return self.votes

class Governance:
    def __init__(self):
        self.proposals = {}
        self.proposal_count = 0

    def create_proposal(self, creator, description):
        """
        Create a new governance proposal
        :param creator: Address of the proposal creator
        :param description: Description of the proposal
        :return: Proposal ID
        """
        self.proposal_count += 1
        proposal = Proposal(self.proposal_count, creator, description)
        self.proposals[self.proposal_count] = proposal
        return self.proposal_count

    def vote_on_proposal(self, proposal_id, voter, option):
        """
        Vote on a governance proposal
        :param proposal_id: ID of the proposal to vote on
        :param voter: Address of the voter
        :param option: Option to vote for
        """
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        proposal = self.proposals[proposal_id]
        proposal.vote(voter, option)

    def end_proposal_voting(self, proposal_id):
        """
        End the voting period for a proposal
        :param proposal_id: ID of the proposal
        """
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        proposal = self.proposals[proposal_id]
        proposal.end_voting()

    def get_proposal_results(self, proposal_id):
        """
        Get the results of a proposal
        :param proposal_id: ID of the proposal
        :return: Voting results
        """
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        proposal = self.proposals[proposal_id]
        return proposal.get_results()

# Example usage
if __name__ == "__main__":
    governance = Governance()

    # Create a new proposal
    proposal_id = governance.create_proposal(creator="0x123", description="Increase block size limit.")
    print(f"Proposal created with ID: {proposal_id}")

    # Vote on the proposal
    governance.vote_on_proposal(proposal_id, voter="0x456", option="Yes")
    governance.vote_on_proposal(proposal_id, voter="0x789", option="No")

    # End voting
    governance.end_proposal_voting(proposal_id)

    # Get results
    results = governance.get_proposal_results(proposal_id)
    print(f"Voting results for proposal {proposal_id}: {results}")
