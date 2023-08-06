from django.db import models
from election.models import CandidateElection
from geography.models import Division
from government.models import Party
from uuslug import slugify


class Election(models.Model):
    """
    A specific contest in a race held on a specific day.
    """
    uid = models.CharField(
        max_length=500,
        primary_key=True,
        editable=False,
        blank=True
    )
    election_type = models.ForeignKey(
        'ElectionType', related_name='elections', on_delete=models.PROTECT)
    candidates = models.ManyToManyField(
        'Candidate', through='CandidateElection')
    race = models.ForeignKey(
        'Race', related_name='elections', on_delete=models.PROTECT)
    party = models.ForeignKey(
        Party, null=True, blank=True, on_delete=models.PROTECT)
    election_day = models.ForeignKey(
        'ElectionDay', related_name='elections', on_delete=models.PROTECT)
    division = models.ForeignKey(
        Division, related_name='elections', on_delete=models.PROTECT)

    def __str__(self):
        base = '{0}, {1}, {2}'.format(
            self.race.office.label,
            self.election_type.label,
            self.election_day.date
        )

        if self.party:
            return '{0} {1}'.format(self.party.label, base)
        else:
            return base

    def save(self, *args, **kwargs):
        """
        **uid**: :code:`{race.uid}_election:{election_day}-{party}`
        """
        if self.party:
            self.uid = '{}_election:{}-{}'.format(
                self.race.uid,
                self.election_day.date,
                slugify(self.party.ap_code)
            )
        else:
            self.uid = '{}_election:{}'.format(
                self.race.uid,
                self.election_day.date
            )
        super(Election, self).save(*args, **kwargs)

    def update_or_create_candidate(
        self, candidate, aggregable=True, uncontested=False
    ):
        """Create a CandidateElection."""
        candidate_election, c = CandidateElection.objects.update_or_create(
            candidate=candidate,
            election=self,
            defaults={
                'aggregable': aggregable,
                'uncontested': uncontested
            }
        )

        return candidate_election

    def delete_candidate(self, candidate):
        """Delete a CandidateElection."""
        CandidateElection.objects.filter(
            candidate=candidate,
            election=self
        ).delete()

    def get_candidates(self):
        """Get all CandidateElections for this election."""
        candidate_elections = CandidateElection.objects.filter(
            election=self
        )

        return [ce.candidate for ce in candidate_elections]

    def get_candidates_by_party(self):
        """
        Get CandidateElections serialized into an object with
        party-slug keys.
        """
        candidate_elections = CandidateElection.objects.filter(
            election=self
        )

        return {
            ce.candidate.party.slug: ce.candidate for ce
            in candidate_elections
        }

    def get_candidate_election(self, candidate):
        """Get CandidateElection for a Candidate in this election."""
        return CandidateElection.objects.get(
            candidate=candidate,
            election=self
        )

    def get_candidate_votes(self, candidate):
        """
        Get all votes attached to a CandidateElection for a Candidate in
        this election.
        """
        candidate_election = CandidateElection.objects.get(
            candidate=candidate,
            election=self
        )

        return candidate_election.votes.all()

    def get_votes(self):
        """
        Get all votes for this election.
        """
        candidate_elections = CandidateElection.objects.filter(
            election=self
        )

        votes = None
        for ce in candidate_elections:
            votes = votes | ce.votes.all()

        return votes

    def get_candidate_electoral_votes(self, candidate):
        """
        Get all electoral votes for a candidate in this election.
        """
        candidate_election = CandidateElection.objects.get(
            candidate=candidate,
            election=self
        )

        return candidate_election.electoral_votes.all()

    def get_electoral_votes(self):
        """
        Get all electoral votes for all candidates in this election.
        """
        candidate_elections = CandidateElection.objects.filter(
            election=self
        )

        electoral_votes = None
        for ce in candidate_elections:
            electoral_votes = electoral_votes | ce.electoral_votes.all()

        return electoral_votes

    def get_candidate_delegates(self, candidate):
        """
        Get all pledged delegates for a candidate in this election.
        """
        candidate_election = CandidateElection.objects.get(
            candidate=candidate,
            election=self
        )

        return candidate_election.delegates.all()

    def get_delegates(self):
        """
        Get all pledged delegates for any candidate in this election.
        """
        candidate_elections = CandidateElection.objects.filter(
            election=self
        )

        delegates = None
        for ce in candidate_elections:
            delegates = delegates | ce.delegates.all()

        return delegates
