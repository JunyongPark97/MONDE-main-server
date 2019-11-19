from django.core import exceptions
from django.db.models.fields.related import ForeignKey
from django.db.utils import ConnectionHandler, ConnectionRouter

connections = ConnectionHandler()
router = ConnectionRouter()


class SpanningForeignKey(ForeignKey):

    def validate(self, value, model_instance):
        if self.rel.parent_link:
            return
        # Call the grandparent rather than the parent to skip validation
        super(ForeignKey, self).validate(value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.rel.to, instance=model_instance)
        qs = self.rel.to._default_manager.using(using).filter(
            **{self.rel.field_name: value}
        )
        qs = qs.complex_filter(self.get_limit_choices_to())
        if not qs.exists():
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.rel.to._meta.verbose_name, 'pk': value,
                    'field': self.rel.field_name, 'value': value,
                },  # 'pk' is included for backwards compatibility
            )

# shopping mall


LUZZIBAG = 1  # is_best -
PAU = 2
JADE = 3  # is_best -
BANAMALL = 4
BEGINNING = 5  # is_best -
BNBURDE = 6  # is_best -
WCONCEPT = 7  # is_best x
GABANGPOP = 8  # is_best x
BAGSHOES = 9
MCLANEE = 10  # is_best -
MJADE = 11
PINKBAG = 12  # is_best -
WHOSBAG = 13
SITE_CHOICES = (
    (LUZZIBAG, 'luzzibag'),
    (PAU, 'paris and you'),
    (JADE, 'jade'),
    (BANAMALL, 'banabana mall'),
    (BEGINNING, 'beginning'),
    (BNBURDE, 'bnburde'),
    (WCONCEPT, 'wconcept'),
    (GABANGPOP, 'gabangpop'),
    (BAGSHOES, 'bagshoes'),
    (MCLANEE, 'mclanee'),
    (MJADE, 'mjade'),
    (PINKBAG, 'pinkbag'),
    (WHOSBAG, 'whosbag'),
)
