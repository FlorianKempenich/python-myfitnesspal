from myfitnesspal.base import MFPBase


class Day(MFPBase):
    def __init__(self, date, meals=None, goals=None, remainings=None, notes=None, water=None):
        self._date = date
        self._meals = meals
        self._goals = goals
        self._remainings = remainings
        self._notes = notes
        self._water = water
        self._totals = None

    def __getitem__(self, value):
        for meal in self._meals:
            if meal.name.lower() == value.lower():
                return meal
        raise KeyError("No meal named '%s' exists for this date" % value)

    def keys(self):
        keys = []
        for meal in self.meals:
            keys.append(meal.name)
        return keys

    @property
    def meals(self):
        return self._meals

    @property
    def entries(self):
        for meal in self._meals:
            for entry in meal.entries:
                yield entry

    @property
    def totals(self):
        if self._totals is None:
            self._compute_totals()

        return self._totals

    @property
    def goals(self):
        return self._goals

    @property
    def remainings(self):
        if self._remainings is None:
            self._compute_remainings()

        return self._remainings

    @property
    def date(self):
        return self._date

    @property
    def notes(self):
        return self._notes()

    @property
    def water(self):
        return self._water()

    def get_as_dict(self):
        return dict(
            (m.name, m.get_as_list(), ) for m in self.meals
        )

    def _compute_totals(self):
        totals = {}
        for entry in self.entries:
            for k, v in entry.nutrition_information.items():
                if k not in totals:
                    totals[k] = v
                else:
                    totals[k] += v

        self._totals = totals

    def _compute_remainings(self):
        remaining = {}
        for k in self.totals:
            if k in self.goals:
                remaining[k] = self.goals[k] - self.totals[k]

        self._remainings = remaining

    def __unicode__(self):
        return u'%s %s' % (
            self.date.strftime('%x'),
            self.totals,
        )
