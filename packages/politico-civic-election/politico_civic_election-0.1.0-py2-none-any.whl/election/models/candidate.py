import uuid

from django.db import models
from election.models import CandidateElection
from entity.models import Person
from government.models import Party


class Candidate(models.Model):
    """
    A person who runs in a race for an office.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    uid = models.CharField(
        max_length=500,
        editable=False,
        blank=True
    )

    race = models.ForeignKey(
        'Race', related_name='candidates', on_delete=models.PROTECT)
    person = models.ForeignKey(
        Person, related_name='candidacies', on_delete=models.PROTECT)
    party = models.ForeignKey(
        Party, related_name='candidates', on_delete=models.PROTECT)
    ap_candidate_id = models.CharField(max_length=255, null=True, blank=True)
    incumbent = models.BooleanField(default=False)
    top_of_ticket = models.ForeignKey(
        'self', null=True, blank=True, related_name='ticket',
        on_delete=models.SET_NULL)
    prospective = models.BooleanField(
        default=False,
        help_text="The candidate has not yet declared her candidacy.")

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`{person.uid}_candidate:{party.uid}-{cycle.ap_code}`
        """
        self.uid = '{}_candidate:{}-{}'.format(
            self.person.uid,
            self.party.uid,
            self.race.cycle.uid
        )
        super(Candidate, self).save(*args, **kwargs)

    def __str__(self):
        return self.uid

    def get_candidate_election(self, election):
        """Get a CandidateElection."""
        return CandidateElection.objects.get(
            candidate=self,
            election=election
        )

    def get_elections(self):
        """Get all elections a candidate is in."""
        candidate_elections = CandidateElection.objects.filter(
            candidate=self
        )

        return [ce.election for ce in candidate_elections]

    def get_election_votes(self, election):
        """Get all votes for this candidate in an election."""
        candidate_election = CandidateElection.objects.get(
            candidate=self,
            election=election
        )

        return candidate_election.votes.all()

    def get_election_electoral_votes(self, election):
        """Get all electoral votes for this candidate in an election."""
        candidate_election = CandidateElection.objects.get(
            candidate=self,
            election=election
        )

        return candidate_election.electoral_votes.all()

    def get_election_delegates(self, election):
        """Get all pledged delegates for this candidate in an election."""
        candidate_election = CandidateElection.objects.get(
            candidate=self,
            election=election
        )

        return candidate_election.delegates.all()

    def get_delegates(self):
        """Get all pledged delegates for this candidate."""
        candidate_elections = CandidateElection.objects.filter(
            candidate=self,
        )

        delegates = None
        for ce in candidate_elections:
            delegates = delegates | ce.delegates.all()

        return delegates
