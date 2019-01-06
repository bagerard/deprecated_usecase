from usecase.privilege import Privilege

sample_privilege1 = Privilege(
        name='SamplePrivilege',
        description='whatever',
        categories=['CAT1', 'CAT2'])


class TestPrivilege:
    def test____init____(self):
        privilege = Privilege(
            name='SamplePrivilege',
            description='whatever',
            categories=['CAT1', 'CAT2'])
        assert privilege.name == 'SamplePrivilege'
        assert privilege.description == 'whatever'
        assert privilege.categories == ['CAT1', 'CAT2']

    def test__to_dict__(self):
        expected = dict(
            name='SamplePrivilege',
            description='whatever',
            categories=['CAT1', 'CAT2'])
        sample_privilege1.to_dict() == expected

    def test__eq__is_equal(self):
        privilege2 = Privilege(
            name=sample_privilege1.name,
            description=None,
            categories=None)
        assert privilege2 == sample_privilege1

    def test__eq__not_equal(self):
        privilege2 = Privilege(
            name="something_else",
            description=None,
            categories=None)
        assert privilege2 != sample_privilege1

    def test____str____(self):
        assert str(sample_privilege1) == 'Privilege: SamplePrivilege'

    def test____hash____is_hashable(self):
        assert hash(sample_privilege1) == hash(sample_privilege1.name)
        assert sample_privilege1 in {sample_privilege1}
