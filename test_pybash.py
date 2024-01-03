from pybash import x__parameters__to__command__array
from pybash import x


def test_x__parameters__to__command__array():
    assert x__parameters__to__command__array('ls -la') == [['ls','-la']]
    assert x__parameters__to__command__array('ls -la | grep 39') == [['ls','-la'], ['grep', '39']]
    assert x__parameters__to__command__array('ls -la | grep "39 Moreten"') == [["ls", "-la"], ["grep", "39 Moreten"]]
    assert x__parameters__to__command__array('ls -la | grep "39 morten" | sed -e "s/39/ni og tredive/g"') == [["ls", "-la"], ["grep", "39 morten"], ["sed", "-e", "s/39/ni og tredive/g"]]



def test_x__successful_piping_of_commands():
    cases = {
        "echo -e 'hallo, Welt\nhello, World\nbonjour Monde' | grep World | sed -e 's/World/world/g'" : "hello, world\n",
    }

    for input in cases:
        expected = cases[input]
        result = x(input)
        actual = result.stdOut
        assert actual == expected
        assert result.returnCode == 0

def test_x__successful_execution_of_commands():
    cases = {
        "echo -n 'Yo, Terra!'" : "Yo, Terra!"
    }

    for input in cases:
        expected = cases[input]
        result = x(input)
        actual = result.stdOut
        assert actual == expected
        assert result.returnCode == 0

"""
def test_x__first_command_failing_returning_2_and_creating_stderr():
    cases = {
        "ls -la asdfasdfasdfasdfasdfasdfasdf" : ["ls: cannot access 'asdfasdfasdfasdf': No such file or directory", 2]
    }

    for input in cases:
        result = x(input)
        assert result.stdOut == ""
        assert result.stdErr == cases[input][0]
        assert result.returnCode == cases[input][1]

"""
