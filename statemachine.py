#!/usr/bin/env python
# Author: Douglas Clowes (douglas.clowes@ansto.gov.au) Aug 2015
# vim: ft=python ts=8 sts=4 sw=4 expandtab autoindent smartindent nocindent
#

# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-instance-attributes
# pylint: disable=missing-docstring
# pylint: disable=global-statement
# pylint: disable=too-few-public-methods
#

class Event(object):
    def __init__(self, name, arglist=None):
        self.name = name
        self.arglist = arglist
    def __repr__(self):
        txt = self.name
        if self.arglist:
            txt = self.name + '(' + ', '.join(self.arglist) + ')'
        return txt
    def __str__(self):
        txt = self.name
        if self.arglist:
            txt = self.name + '(' + ', '.join(self.arglist) + ')'
        return txt

class State(object):
    def __init__(self, name, base_list=None):
        self.name = name
        if base_list == None:
            self.base_list = []
        else:
            self.base_list = base_list

    def __repr__(self):
        if len(self.base_list) > 0:
            return self.name + '(' + ', '.join(self.base_list) + ')'
        else:
            return self.name

class Transition(object):
    def __init__(self, source, event, actions=None, targets=None):
        self.source = source
        self.event = event
        self.actions = actions
        self.targets = targets

    def __repr__(self):
        return ", ".join([self.source, self.event, repr(self.actions), repr(self.targets)])

class Classifier(object):
    def __init__(self, source, event, actions=None, targets=None):
        self.source = source
        self.event = event
        self.actions = actions
        self.targets = targets

    def __repr__(self):
        return ", ".join([self.source, self.event, repr(self.actions), repr(self.targets)])

class Action(object):
    def __init__(self, name, code_type, code_text=None):
        self.name = name
        self.code_type = code_type
        self.code_text = code_text

    def __repr__(self):
        return "%s(%s) {%s}" % (self.name, self.code_type, self.code_text)

class Test(object):
    def __init__(self, tests):
        self.tests = tests

    def __repr__(self):
        return ", ".join(self.tests)

class StateMachine(object):
    def __init__(self, name):
        self.name = name
        self.uname = name.upper()
        self.actions = []
        self.events = []
        self.states = []
        self.tests = []
        self.transitions = []
        self.classifiers = []

    def __repr__(self):
        text = "name = %s" % repr(self.name)
        text += ", uname = %s" % repr(self.uname)
        text += ", states = [%s]" % ', '.join([repr(s) for s in self.states])
        text += ", events = [%s]" % ', '.join([repr(s) for s in self.events])
        text += ", classifiers = [%s]" % ', '.join([repr(s) for s in self.classifiers])
        text += ", transitions = [%s]" % ', '.join([repr(s) for s in self.transitions])
        text += ", tests = [%s]" % ', '.join([repr(s) for s in self.tests])
        text += ", actions = [%s]" % ', '.join([repr(s) for s in self.actions])
        return '{ ' + text + ' }'

    def addEvent(self, event):
        assert isinstance(event, Event)
        if event not in self.events:
            self.events.append(event)

    def addState(self, state):
        assert isinstance(state, State)
        if state not in self.states:
            self.states.append(state)

    def addTransition(self, transition):
        assert isinstance(transition, Transition)
        assert transition.source in [s.name for s in self.states]
        assert transition.event in [e.name for e in self.events]
        if (transition.source, transition.event) not in [(t.source, t.event) for t in self.transitions]:
            self.transitions.append(transition)
        else:
            print "Duplicate transition:", transition

    def addClassifier(self, classifier):
        assert isinstance(classifier, Classifier)
        assert classifier.source in [s.name for s in self.states]
        assert classifier.event in [e.name for e in self.events]
        if (classifier.source, classifier.event) not in [(t.source, t.event) for t in self.classifiers]:
            self.classifiers.append(classifier)
        else:
            print "Duplicate classifier:", classifier

    def addAction(self, action):
        assert isinstance(action, Action)
        self.actions.append(action)

    def addTest(self, test):
        assert isinstance(test, Test)
        for item in test.tests:
            assert item in [s.name for s in self.states] + [e.name for e in self.events]
        assert test.tests[0] in [s.name for s in self.states]
        assert test.tests[-1] in [s.name for s in self.states]
        self.tests.append(test)

    def getEvent(self, name):
        for e in self.events:
            if e.name == name:
                return e
        return None

    def getState(self, name):
        for s in self.states:
            if s.name == name:
                return s
        return None

    def printit(self):
        print "StateMachine:", self.name
        print "States:", ", ".join([repr(s) for s in self.states])
        print "Events:", ", ".join([repr(s) for s in self.events])
        for c in self.classifiers:
            print "Classifier:", c
        for t in self.transitions:
            print "Transition:", t
        for a in self.actions:
            print "Action:", a
        for t in self.tests:
            print "Test:", t

class StateMachine_Text(StateMachine):
    def __init__(self, other):
        StateMachine.__init__(self, other.name)
        if isinstance(other, StateMachine):
            self.name = other.name[:]
            self.actions = other.actions[:]
            self.events = other.events[:]
            self.states = other.states[:]
            self.tests = other.tests[:]
            self.transitions = other.transitions[:]
            self.classifiers = other.classifiers[:]

    def Inheritance(self):
        base_states = {}
        for derived in [state for state in self.states if len(state.base_list) > 0]:
            for b in derived.base_list:
                base_states[b] = None
            replaced = [sc.event for sc in self.classifiers + self.transitions if sc.source == derived.name]
            print "Derived:", derived, replaced
            inherited = [sc for sc in self.classifiers + self.transitions if sc.source in derived.base_list]
            print "Inherited:", derived, inherited
            virtual = [i for i in inherited if i.event not in replaced]
            print "Virtual:", derived, virtual
            for item in virtual:
                if isinstance(item, Classifier):
                    self.addClassifier(Classifier(derived.name, item.event, item.actions, item.targets))
                else:
                    self.addTransition(Transition(derived.name, item.event, item.actions, item.targets))
        target_states = {}
        for s in self.transitions:
            for t in s.targets:
                target_states[t] = None
        print "Targets:", target_states
        ghosts = [s for s in self.transitions if s.source not in target_states]
        print "Ghosts:", ghosts
        print "Bases:", base_states
        for s in ghosts:
            if s.source in base_states:
                self.transitions.remove(s)
                print "Removed:", s

    def TextStateMachine(self):
        the_states = sorted([s.name for s in self.states])
        the_events = sorted([e.name for e in self.events])
        txt = ['STATEMACHINE %s {' % self.name]
        txt += ['  STATES\n    %s;' % ',\n    '.join(the_states)]
        txt += ['  EVENTS\n    %s;' % ',\n    '.join(the_events)]
        for state in the_states:
            s = self.getState(state)
            if s and len(s.base_list) > 0:
                txt += ['  State %s (%s) {' % (state, ', '.join(s.base_list))]
            else:
                txt += ['  State %s {' % state]
            the_blocks = [b for b in self.classifiers if b.source == state]
            the_blocks += [b for b in self.transitions if b.source == state]
            for block in the_blocks:
                line = '%s' % block.event
                if isinstance(block, Classifier):
                    line += ' --> %s' % ', '.join(block.actions)
                    if len(block.targets) > 0:
                        next_events = sorted([e[0] for e in block.targets])
                        line += ' => %s' % ', '.join(next_events)
                else:
                    if len(block.actions) > 0:
                        line += ' -> %s' % ', '.join(block.actions)
                    if len(block.targets) > 0:
                        line += ' => %s' % ', '.join(block.targets)
                txt += ['    %s;' % line]
            txt += ['  }']
        for action in sorted(self.actions, key=lambda action: action.name.lower()):
            print "##Action:", action
            txt += ['  CODE %s %s {' % (action.code_type, action.name)]
            for action_item in action.code_text:
                txt += ['    @%s' % action_item[0]]
                for line in action_item[1]:
                    txt += [line]
                txt += ['    @END']
            txt += ['  }']
        for test in self.tests:
            txt += ['  Test %s;' % ',\n    '.join(test.tests)]
        txt += ['}']
        return txt

class StateMachine_HTML(StateMachine_Text):
    def __init__(self, other):
        StateMachine_Text.__init__(self, other)
        self.Inheritance()

    def StateTable1(self):
        the_states = sorted([s.name for s in self.states])
        txt = ['<TABLE BORDER=1>']
        txt += ['<TR>']
        txt += ['<TH><TABLE WIDTH=100%>']
        txt += ['<TR><TD ALIGN="right">Next(&gt;)</TD></TR>']
        txt += ['<TR><TD ALIGN="left">Current(v)</TD></TR>']
        txt += ['</TABLE></TH>']
        for s_next in the_states:
            txt += ['<TH>%s</TH>' % s_next]
        txt += ['</TR>\n']
        for s_curr in the_states:
            txt += ['<TR><TD VALIGN="top"><B>%s</B></TD>' % s_curr]
            for s_next in the_states:
                txt += ['<TD VALIGN="top"><TABLE>']
                if s_curr == s_next:
                    for block in self.classifiers:
                        if block.source == s_curr:
                            event = block.event
                            action = ',<BR/>'.join(block.actions)
                            txt += ['<TR><TD VALIGN="top"><B>%s</B></TD>' % event]
                            txt += ['<TD VALIGN="top">%s</TD></TR>' % action]
                for block in self.transitions:
                    if block.source == s_curr and s_next in block.targets:
                        event = block.event
                        action = ',<BR/>'.join(block.actions)
                        txt += ['<TR><TD VALIGN="top"><B>%s</B></TD>' % event]
                        txt += ['<TD VALIGN="top">%s</TD></TR>' % action]
                txt += ['</TABLE></TD>']
            txt += ['</TR>']
        txt += ['</TABLE>']
        return txt

    def StateTable2(self):
        the_states = sorted([s.name for s in self.states])
        the_events = sorted([e.name for e in self.events])
        txt = ['<TABLE BORDER=1>']
        txt += ['<TR>']
        txt += ['<TH><TABLE WIDTH=100%>']
        txt += ['<TR><TD VALIGN="right">State(&gt;)</TD></TR>']
        txt += ['<TR><TD VALIGN="left">Event(v)</TD></TR>']
        txt += ['</TABLE></TH>']
        for s in the_states:
            txt += ['<TH>%s</TH>' % s]
        txt += ['</TR>\n']
        for e in the_events:
            txt += ['<TR><TD VALIGN="top"><B>%s</B></TD>' % e]
            for s in the_states:
                txt += ['<TD VALIGN="top"><TABLE>']
                the_blocks = [b for b in self.classifiers + self.transitions if b.source == s]
                for block in the_blocks:
                    if e == block.event:
                        action = ',<BR/>'.join(block.actions)
                        next_state = ''
                        if isinstance(block, Transition):
                            next_state = '<B>' + ',<BR>'.join(block.targets) + '</B>'
                        txt += ['<TR><TD VALIGN="top">%s</TD><TD VALIGN="top">%s</TD></TR>' % (action, next_state)]
                txt += ['</TABLE></TD>']
            txt += ['</TR>']
        txt += ['</TABLE>']
        return txt

    def StateTable3(self):
        the_states = sorted([s.name for s in self.states])
        the_events = sorted([e.name for e in self.events])
        txt = ['<TABLE BORDER=1>\n']
        txt += ['<TR>']
        for t in ['State', 'Event', 'Actions', 'Next']:
            txt += ['<TH>%s</TH>' % t]
        txt += ['</TR>\n']
        for s in the_states:
            for e in the_events:
                the_blocks = [b for b in self.classifiers + self.transitions if b.source == s]
                for block in the_blocks:
                    if e == block.event:
                        txt += ['<TR>']
                        txt += ['<TD VALIGN="top"><B>%s</B></TD>' % s]
                        txt += ['<TD VALIGN="top"><B>%s</B></TD>' % e]
                        action = ',<BR/>'.join(block.actions)
                        txt += ['<TD VALIGN="top">%s</TD>' % action]
                        next_state = ''
                        if isinstance(block, Transition):
                            next_state = '<B>' + ',<BR>'.join(block.targets) + '</B>'
                        else:
                            next_state = s
                        txt += ['<TD VALIGN="top">%s</TD>' % next_state]
                        txt += ['</TR>\n']
        txt += ['</TABLE>\n']
        return txt

    def DotStateMachine(self):
        the_states = sorted([s.name for s in self.states])
        txt = ['digraph G {']
        txt += ['  size="11,8";']
        txt += ['  ratio="expand";']
        txt += ['  rankdir=LR;']
        txt += ['  node [shape=plaintext];']
        txt += ['  labelloc="t";']
        txt += ['  label=<<B>%s</B>>' % self.name]
        txt += ['']
        for state in the_states:
            label = ['<TABLE><TR><TD PORT="f0"><B>']
            label += ['%s' % state]
            label += ['</B></TD></TR>']
            the_blocks = [b for b in self.classifiers if b.source == state]
            the_blocks += [b for b in self.transitions if b.source == state]
            for idx, block in enumerate(the_blocks):
                label += ['<TR><TD><TABLE>']
                label += ['<TR><TD PORT="f%d">' % (idx + 1)]
                label += ['<B>%s</B></TD></TR>' % block.event]
                if len(block.actions) > 0:
                    label += ['<TR><TD>%s</TD></TR>' % '</TD></TR><TR><TD>'.join(block.actions)]
                label += ['</TABLE></TD></TR>']
            label += ['</TABLE>']
            txt += ['  %s[label=<%s>];' % (state, ''.join(label))]
            for idx, block in enumerate(the_blocks):
                if isinstance(block, Transition):
                    for t in block.targets:
                        txt += ['    %s:f%d -> %s:f0;' % (state, idx + 1, t)]
        txt += ['}']
        return txt

    def DotStateMachine2(self):
        the_states = sorted([s.name for s in self.states])
        txt = ['digraph G {']
        txt += ['  size="11,8";']
        txt += ['  ratio="expand";']
        txt += ['  rankdir=LR;']
        txt += ['  node [shape=plaintext];']
        txt += ['  labelloc="t";']
        txt += ['  label=<<B>%s</B>>' % self.name]
        txt += ['']
        colors = ['red', 'green', 'blue', 'orange', 'purple', 'magenta', 'cyan', 'yellow']
        for state in the_states:
            label = ['<TABLE><TR><TD PORT="%s"><B>' % state]
            label += ['%s' % state]
            label += ['</B></TD></TR>']
            the_blocks = [b for b in sorted(self.classifiers) if b.source == state]
            the_blocks += [b for b in sorted(self.transitions) if b.source == state]
            idx = 0
            for block in the_blocks:
                label += ['<TR><TD><TABLE>']
                label += ['<TR><TD PORT="%s">' % block.event]
                label += ['<B>%s</B></TD></TR>' % block.event]
                if len(block.actions) > 0:
                    label += ['<TR><TD>%s</TD></TR>' % '</TD></TR><TR><TD>'.join(block.actions)]
                label += ['</TABLE></TD></TR>']
            label += ['</TABLE>']
            txt += ['  %s[label=<%s>];' % (state, ''.join(label))]
            for block in the_blocks:
                if isinstance(block, Transition):
                    for t in block.targets:
                        txt += ['    %s:%s -> %s:%s;' % (state, block.event, t, t)]
                else:
                    style = 'dir=both;arrowtail=inv;style=dotted;color=%s' % colors[idx]
                    idx += 1
                    if idx >= len(colors):
                        idx = 0
                    for t in block.targets:
                        if t[0] in [b.event for b in the_blocks]:
                            txt += ['    %s:%s -> %s:%s[%s];' % (state, block.event, state, t[0], style)]
        txt += ['}']
        return txt

class StateMachine_Python(StateMachine_Text):
    def __init__(self, other):
        StateMachine_Text.__init__(self, other)
        self.Inheritance()

    def Generate_Python(self):
        the_states = sorted([s.name for s in self.states])
        the_events = sorted([e.name for e in self.events])
        action_list = []
        classifier_list = []
        test_list = []
        txt = []
        txt += ['# Generated by program']
        txt += ['# pylint: disable=invalid-name']
        txt += ['# pylint: disable=line-too-long']
        txt += ['# pylint: disable=too-many-lines']
        txt += ['# pylint: disable=too-many-locals']
        txt += ['# pylint: disable=too-many-branches']
        txt += ['# pylint: disable=too-many-statements']
        txt += ['# pylint: disable=too-many-return-statements']
        txt += ['# pylint: disable=missing-docstring']
        txt += ['# pylint: disable=global-statement']
        txt += ['# pylint: disable=unused-argument']
        func_name = 'StateSwitch_%s'  % self.name
        txt += ['def %s(context, state, event):' % func_name]
        txt += ['    next_state = state']
        txt += ['    next_event = None']
        for s in the_states:
            txt += ['    if state == "%s":' % s]
            for e in the_events:
                the_blocks = [b for b in self.classifiers + self.transitions if b.source == s]
                for block in the_blocks:
                    if e == block.event:
                        txt += ['        if event == "%s":' % e]
                        for action in block.actions:
                            if isinstance(block, Classifier):
                                txt += ['            next_event = %s(context, state, event)' % (action)]
                                if action not in [c[0] for c in classifier_list]:
                                    classifier_list.append((action, block.targets))
                            else:
                                txt += ['            %s(context, state, event)' % (action)]
                                if action not in action_list:
                                    action_list.append(action)
                        if isinstance(block, Transition) and len(block.targets) > 0:
                            txt += ['            next_state = "%s"' % (block.targets[0])]
                            test_list.append((s, e, block.targets[0]))
                        else:
                            test_list.append((s, e, s))
                        txt += ['            return (next_state, next_event, 1)']
            txt += ['        return (next_state, next_event, 0)']
        txt += ['    return (next_state, next_event, 0)']
        txt += ['']
        txt += ['def RunStateSwitch_%s(context, state, event):' % self.name]
        txt += ['    next_state = state']
        txt += ['    next_event = event']
        txt += ['    rule_count = 0']
        txt += ['    while next_event is not None:']
        txt += ['        state_event = StateSwitch_%s(context, state, next_event)' % self.name]
        txt += ['        next_event = state_event[1]']
        txt += ['        rule_count = rule_count + state_event[2]']
        txt += ['    next_state = state_event[0]']
        txt += ['    if next_state != state:']
        txt += ['        state_event = StateSwitch_%s(context, state, "Exit")' % self.name]
        txt += ['        state_event = StateSwitch_%s(context, next_state, "Entry")' % self.name]
        txt += ['    return (next_state, next_event, rule_count)']
        txt += ['']
        slen = max([len(s) for s in the_states])
        elen = max([len(e) for e in the_events])
        txt += ['if __name__ == "__main__":']
        print "Classifiers:", classifier_list
        for action in classifier_list:
            txt += ['    def %s(context, state, event):' % action[0]]
            line = '"State %%-%ds event %%-%ds: %s" %% (state, event)' % (slen, elen, action[0])
            txt += ['        print %s' % line]
            txt += ['        return "%s"' % action[1][0][0]]
        print "Actions:", action_list
        for action in action_list:
            txt += ['    def %s(context, state, event):' % action]
            line = '"State %%-%ds event %%-%ds: %s" %% (state, event)' % (slen, elen, action)
            txt += ['        print %s' % line]
        print "Tests:", test_list
        txt += ['    def TestStateSwitch_%s():' % self.name]
        for test in test_list:
            s1 = test[0]
            ev = test[1]
            s2 = test[2]
            txt += ['        state_event = %s("Context", "%s", "%s")' % (func_name, s1, ev)]
            txt += ['        assert state_event[2] > 0']
            txt += ['        assert state_event[0] == "%s"' % (s2)]
        txt += ['    TestStateSwitch_%s()' % self.name]
        txt += ['    print "TestStateSwitch_%s() passed"' % self.name]
        for test in self.tests:
            print "Test::", test
            txt += ['    state_event = ("%s", None, 0)' % test.tests[0]]
            for t in test.tests:
                if t in the_states:
                    txt += ['    assert state_event[0] == "%s"' % t]
                else:
                    txt += ['    state_event = %s("Context", state_event[0], "%s")' % (func_name, t)]
                    txt += ['    assert state_event[2] > 0']
            txt += ['    print "Test Passed: %s"' % repr(test)]
        txt2 = ['else:']
        for action in action_list:
            the_blocks = [b for b in self.actions if b.name == action and b.code_type == 'action']
            if len(the_blocks) == 0:
                continue
            txt2 += ['    def %s (context, state, event):' % action]
            print "##The Blocks:", the_blocks
            for code_block in the_blocks:
                print "##CodeBlock:", code_block
                print "##CodeText:", code_block.code_text
                for code_text in [c[1] for c in code_block.code_text if c[0] == 'PYTHON']:
                    print "##CodeText:", code_text
                    # Calculate the minimum white space for indent adjustment
                    min_wh = min([len(s) - len(s.lstrip(' ')) for s in code_text])
                    for code in code_text:
                        print "##Code:", code[min_wh:]
                        txt2 += ['        ' + code[min_wh:]]
        if len(txt2) > 1:
            txt += txt2
        txt += ['# vim: ft=python ts=8 sts=4 sw=4 expandtab autoindent smartindent nocindent']
        return txt

class StateMachine_TCL(StateMachine_Text):
    def __init__(self, other):
        StateMachine_Text.__init__(self, other)
        self.Inheritance()

    def Generate_TCL(self):
        the_states = sorted([s.name for s in self.states])
        the_events = sorted([e.name for e in self.events])
        action_list = []
        classifier_list = []
        test_list = []
        func_name = 'StateSwitch_%s'  % self.name
        txt = ['proc %s {context state event} {' % func_name]
        txt += ['    set next_state ${state}']
        txt += ['    set next_event {}']
        for s in the_states:
            txt += ['    if {${state} == "%s"} {' % s]
            for e in the_events:
                the_blocks = [b for b in self.classifiers + self.transitions if b.source == s]
                for block in the_blocks:
                    if e == block.event:
                        txt += ['        if {${event} == "%s"} {' % e]
                        for action in block.actions:
                            if isinstance(block, Classifier):
                                txt += ['            set next_event [%s ${context} ${state} ${event}]' % (action)]
                                if action not in [c[0] for c in classifier_list]:
                                    classifier_list.append((action, block.targets))
                            else:
                                txt += ['            %s ${context} ${state} ${event}' % (action)]
                                if action not in action_list:
                                    action_list.append(action)
                        if isinstance(block, Transition) and len(block.targets) > 0:
                            txt += ['            set next_state "%s"' % (block.targets[0])]
                            test_list.append((s, e, block.targets[0]))
                        else:
                            test_list.append((s, e, s))
                        txt += ['            return [list ${next_state} ${next_event} 1]']
                        txt += ['        }']
            txt += ['        return [list ${next_state} ${next_event} 0]']
            txt += ['    }']
        txt += ['    return [list ${next_state} ${next_event} 0]']
        txt += ['}', '']
        txt += ['proc RunStateSwitch_%s {context state event} {' % self.name]
        txt += ['    set next_state ${state}']
        txt += ['    set next_event ${event}']
        txt += ['    set rule_count 0']
        txt += ['    while { ${next_event} != {} } {']
        txt += ['        set state_event [StateSwitch_%s ${context} ${state} ${next_event}]' % self.name]
        txt += ['        set next_event [lindex ${state_event} 1]']
        txt += ['        set rule_count [expr {${rule_count} + [lindex ${state_event} 2]}]']
        txt += ['    }']
        txt += ['    set next_state [lindex ${state_event} 0]']
        txt += ['    if { ${next_state} != ${state} } {']
        txt += ['        set state_event [StateSwitch_%s ${context} ${state} "Exit"]' % self.name]
        txt += ['        set state_event [StateSwitch_%s ${context} ${next_state} "Entry"]' % self.name]
        txt += ['    }']
        txt += ['    return [list ${next_state} ${next_event} ${rule_count}]']
        txt += ['}', '']
        slen = max([len(s) for s in the_states])
        elen = max([len(e) for e in the_events])
        txt += ['if { "[lindex [split [info nameofexecutable] "/"] end]" == "tclsh"} {']
        print "Classifiers:", classifier_list
        for action in classifier_list:
            txt += ['    proc %s {context state event} {' % action[0]]
            line = 'State [format "%%-%ds" ${state}] event [format "%%-%ds" ${event}]: %s' %\
                    (slen, elen, action[0])
            txt += ['        puts "%s"' % line]
            txt += ['        return "%s"' % action[1][0][0]]
            txt += ['    }']
        print "Actions:", action_list
        for action in action_list:
            txt += ['    proc %s {context state event} {' % action]
            line = 'State [format "%%-%ds" ${state}] event [format "%%-%ds" ${event}]: %s' %\
                    (slen, elen, action)
            txt += ['        puts "%s"' % line]
            txt += ['    }']
        print "Tests:", test_list
        for test in test_list:
            s1 = test[0]
            ev = test[1]
            s2 = test[2]
            txt += ['    set state_event [%s "Ctx" "%s" "%s"]' % (func_name, s1, ev)]
            txt += ['    if {[lindex ${state_event} 2] <= 0} {error "count fail!"}']
            txt += ['    if {[lindex ${state_event} 0] != "%s"} {error "state fail!"}' % (s2)]
        txt += ['    puts "TestStateSwitch_%s() passed"' % self.name]
        for test in self.tests:
            print "Test::", test
            txt += ['    set state_event [list "%s" {} 0]' % test.tests[0]]
            for t in test.tests:
                if t in the_states:
                    txt += ['    if {[lindex ${state_event} 0] != "%s"} {error "state fail!"}' % t]
                else:
                    txt += ['    set state_event [%s "Ctx" [lindex ${state_event} 0] "%s"]' % (func_name, t)]
                    txt += ['    if {[lindex ${state_event} 2] <= 0} {error "count fail!"}']
            txt += ['    puts "Test Passed: %s"' % repr(test)]
        txt2 = ['} else {']
        for action in action_list:
            the_blocks = [b for b in self.actions if b.name == action and b.code_type == 'action']
            if len(the_blocks) == 0:
                continue
            txt2 += ['    proc %s {context state event} {' % action]
            print "##The Blocks:", the_blocks
            for code_block in the_blocks:
                print "##CodeBlock:", code_block
                print "##CodeText:", code_block.code_text
                for code_text in [c[1] for c in code_block.code_text if c[0] == 'TCL']:
                    print "##CodeText:", code_text
                    # Calculate the minimum white space for indent adjustment
                    min_wh = min([len(s) - len(s.lstrip(' ')) for s in code_text])
                    for code in code_text:
                        print "##Code:", code[min_wh:]
                        txt2 += ['        ' + code[min_wh:]]
            txt2 += ['    }']
        if len(txt2) > 1:
            txt += txt2
        txt += ['}']
        return txt

class StateMachine_GCC(StateMachine_Text):
    def __init__(self, other):
        StateMachine_Text.__init__(self, other)
        self.Inheritance()

    def mkFunc(self, name=None):
        if name:
            return  'FSM_%s_%s' % (self.uname, name)
        return 'FSM_%s' % (self.uname)

    def mkName(self, name=None):
        if name:
            return  'FSM_%s_%s' % (self.uname, name)
        return 'FSM_%s' % (self.uname)

    def mkState(self, name=None):
        if name:
            return  'FSM_%s_STATE_%s' % (self.uname, name)
        return  'FSM_%s_STATE' % (self.uname)

    def mkEvent(self, name=None):
        if name:
            return  'FSM_%s_EVENT_%s' % (self.uname, name)
        return  'FSM_%s_EVENT' % (self.uname)

    def mkAction(self, name=None):
        if name:
            return  'FSM_%s_ACTION_%s' % (self.uname, name)
        return  'FSM_%s_ACTION' % (self.uname)

    def Generate_C(self):
        the_states = sorted([s.name for s in self.states])
        the_events = sorted([e.name for e in self.events])
        the_actions = []
        classifier_list = {}
        the_blocks = [b for b in self.classifiers + self.transitions]
        max_actions = 0
        for block in the_blocks:
            if len(block.actions) > max_actions:
                max_actions = len(block.actions)
            for action in block.actions:
                if action not in the_actions:
                    the_actions.append(action)
        the_actions = sorted(the_actions)
        uname = self.name.upper()
        hdr = ['#ifndef %s_H' % uname]
        hdr += ['#define %s_H' % uname]
        #hdr += ['#include "statemachine.h"', '']
        tkns = []
        tkns += [('NUM_STATES', len(the_states))]
        tkns += [('NUM_EVENTS', len(the_events))]
        tkns += [('NUM_TRANS', len(the_blocks))]
        tkns += [('NUM_ACTIONS', len(the_actions))]
        tkns += [('MAX_ACTIONS', max_actions)]
        stts = []
        for idx, state in enumerate(the_states):
            stts += [(state, idx + 1)]
        evts = []
        for idx, event in enumerate(the_events):
            evts += [(event, idx + 1)]
        acts = []
        for idx, action in enumerate(the_actions):
            acts += [(action, idx + 1)]
        print "tkns:", tkns
        print "stts:", stts
        print "evts:", evts
        print "acts:", acts
        for item in tkns:
            hdr += ['#define %s %d'\
                    % (self.mkName(item[0]), item[1])]
        # States
        hdr += ['', '/* States */']
        hdr += ['typedef const struct %s_t *%s;'\
                % (self.mkState(), self.mkState())]
        for item in stts:
            hdr += ['extern  const %s %s;'\
                    % (self.mkState(), self.mkState(item[0]))]
        # Events
        hdr += ['', '/* Events */']
        hdr += ['typedef const struct %s_t *%s;'\
                % (self.mkEvent(), self.mkEvent())]
        for item in evts:
            hdr += ['extern  const %s %s;'\
                    % (self.mkEvent(), self.mkEvent(item[0]))]
        # Actions
        hdr += ['', '/* Actions */']
        hdr += ['typedef const struct %s_t *%s;'\
                % (self.mkAction(), self.mkAction())]
        for item in acts:
            hdr += ['extern  const %s %s;'\
                    % (self.mkAction(), self.mkAction(item[0]))]
        # Epilog
        hdr += ['', '/* Epilog */']
        hdr += ['typedef struct %s_t *%s; /* instance */'\
                % (self.mkName(), self.mkName())]
        hdr += ['typedef %s (*%s)('\
                % (self.mkState(), self.mkFunc('Action'))]
        hdr += ['    %s smi,' % self.mkName()]
        hdr += ['    %s state, ' % self.mkState()]
        hdr += ['    %s event);' % self.mkEvent()]
        hdr += ['typedef %s (*%s)('\
                % (self.mkEvent(), self.mkFunc('Classify'))]
        hdr += ['    %s smi,' % self.mkName()]
        hdr += ['    %s state, ' % self.mkState()]
        hdr += ['    %s event);' % self.mkEvent()]
        hdr += ['%s %s(%s initial);'\
                % (self.mkName(), self.mkFunc('Make'), self.mkEvent())]
        hdr += ['void %s(%s smi);' % (self.mkName('Kill'), self.mkFunc())]
        hdr += ['void %s(%s smi,'\
                % (self.mkFunc('Run'), self.mkName())]
        hdr += ['    %s ev);'\
                % (self.mkEvent())]
        hdr += ['void %s(%s smi,'\
                % (self.mkFunc('SetAction'), self.mkName())]
        hdr += ['    %s action,'\
                % (self.mkAction())]
        hdr += ['    %s af);'\
                % (self.mkFunc('Action'))]
        hdr += ['void %s(%s smi,'\
                % (self.mkFunc('SetClassify'), self.mkName())]
        hdr += ['    %s action,'\
                % (self.mkAction())]
        hdr += ['    %s af);'\
                % (self.mkFunc('Classify'))]
        #hdr += ['extern fsmStateMachine fsm_%s;' % self.name]
        hdr += ['', '#endif /* %s_H */' % uname]

        txt = []
        txt += ['#include <stdlib.h>']
        txt += ['#include <stdio.h>']
        txt += ['']
        tab_idx = 0
        act_idx = 0
        evt_idx = 0
        # States
        txt += ['', '/* States */']
        txt += ['struct %s_t {' % self.mkState()]
        txt += ['    char *name;']
        txt += ['    int  index;']
        txt += ['};']
        txt += ['static const struct %s_t state_pointers [] = {' % self.mkState()]
        txt += ['    { NULL, %s },' % len(stts)]
        for item in stts:
            txt += ['    { "%s", %d },'\
                    % (item[0], item[1])]
        txt += ['    { NULL, 0 }']
        txt += ['};']
        for item in stts:
            txt += ['const %s %s = &state_pointers[%d];'\
                    % (self.mkState(), self.mkState(item[0]), item[1])]
        txt += ['enum {']
        for item in stts:
            txt += ['    e%s = %s,' % (self.mkState(item[0]), item[1])]
        txt += ['};']
        # Events
        txt += ['', '/* Events */']
        txt += ['struct %s_t {' % self.mkEvent()]
        txt += ['    char *name;']
        txt += ['    int  index;']
        txt += ['};']
        txt += ['static const struct %s_t event_pointers [] = {' % self.mkEvent()]
        txt += ['    { NULL, %s },' % len(evts)]
        for item in evts:
            txt += ['    { "%s", %d },'\
                    % (item[0], item[1])]
        txt += ['    { NULL, 0 }']
        txt += ['};']
        for item in evts:
            txt += ['const %s %s = &event_pointers[%d];'\
                    % (self.mkEvent(), self.mkEvent(item[0]), item[1])]
        txt += ['enum {']
        for item in evts:
            txt += ['    e%s = %s,' % (self.mkEvent(item[0]), item[1])]
        txt += ['};']
        # Actions
        txt += ['', '/* Actions */']
        txt += ['struct %s_t {' % self.mkAction()]
        txt += ['    char *name;']
        txt += ['    int  index;']
        txt += ['};']
        txt += ['static const struct %s_t action_pointers [] = {' % self.mkAction()]
        txt += ['    { NULL, %s },' % len(evts)]
        for item in acts:
            txt += ['    { "%s", %d },'\
                    % (item[0], item[1])]
        txt += ['    { NULL, 0 }']
        txt += ['};']
        for item in acts:
            txt += ['const %s %s = &action_pointers[%d];'\
                    % (self.mkAction(), self.mkAction(item[0]), item[1])]
        txt += ['enum {']
        for item in acts:
            txt += ['    e%s = %s,' % (self.mkAction(item[0]), item[1])]
        txt += ['};']
        #
        txt += ['']
        act_txt = ['/* TODO: describe the action_table */']
        act_txt += ['static const struct %s_t * const action_table[] = {' % self.mkAction()]
        evt_txt = ['/* TODO: describe the event_table */']
        evt_txt += ['static const struct %s_t * event_table[] = {' % self.mkEvent()]
        map_txt = ['/* TODO: describe the map_table */']
        map_txt += ['static int map_table[] = {', '    0,']
        tab_txt = ['/* TODO: describe the tab_table */']
        tab_txt += ['typedef struct fsmTransTab_t fsmTransTab;']
        tab_txt += ['typedef enum {']
        tab_txt += ['    fsmActionClass = 1, /* Classifier Action Entry */']
        tab_txt += ['    fsmActionTrans = 2  /* Transition Action Entry */']
        tab_txt += ['} fsmActionType;']
        tab_txt += ['struct fsmTransTab_t {']
        tab_txt += ['    %s si; /* Input State */' % self.mkState()]
        tab_txt += ['    %s ei; /* Input Event */' % self.mkEvent()]
        tab_txt += ['    fsmActionType ac_type; /* Classifier or Transition */']
        tab_txt += ['    union {']
        tab_txt += ['        struct { /* Classifier Action Entry */']
        tab_txt += ['            int ac_class; /* Action Classifier */']
        tab_txt += ['            int ev_start; /* First output Event */']
        tab_txt += ['            int ev_count; /* Number of candidates */']
        tab_txt += ['        };']
        tab_txt += ['        struct { /* Transition Action Entry */']
        tab_txt += ['            %s so;        /* Output State */' % self.mkState()]
        tab_txt += ['            int ac_start; /* First Action */']
        tab_txt += ['            int ac_count; /* Number of Actions */']
        tab_txt += ['        };']
        tab_txt += ['    };']
        tab_txt += ['};']
        tab_txt += ['static fsmTransTab trans_table[] = {']
        for state in the_states:
            map_txt += ['    %d, /* %s */' % (tab_idx, state)]
            for event in the_events:
                for block in the_blocks:
                    if block.source == state:
                        if block.event == event:
                            act_cnt = len(block.actions)
                            for item in block.actions:
                                act_txt += ['    &action_pointers[e%s],' % self.mkAction(item)]
                            target = state
                            if isinstance(block, Transition) and len(block.targets) > 0:
                                target = block.targets[0]
                            line = ''
                            line += '    { /* %d */\n' % (tab_idx)
                            line += '        .si=&state_pointers[e%s],\n' % (self.mkState(state))
                            line += '        .ei=&event_pointers[e%s],\n' % (self.mkEvent(event))
                            if isinstance(block, Transition):
                                line += '        .ac_type=fsmActionTrans,\n'
                                line += '        .so=&state_pointers[e%s],\n' % self.mkState(target)
                                line += '        .ac_start=%d,\n' % act_idx
                                line += '        .ac_count=%d,\n' % act_cnt
                            else:
                                evt_cnt = len(block.targets)
                                for item in block.targets:
                                    evt_txt += ['    &event_pointers[e%s],' % self.mkEvent(item[0])]
                                line += '        .ac_type=fsmActionClass,\n'
                                line += '        .ac_class=e%s,\n' % self.mkAction(block.actions[0])
                                line += '        .ev_start=%d,\n' % evt_idx
                                evt_idx += evt_cnt
                                line += '        .ev_count=%s,\n' % evt_cnt
                                for action in block.actions:
                                    if action not in classifier_list:
                                        classifier_list[action] = block.targets[0]
                            line += '    },'
                            tab_txt += [line]
                            tab_idx += 1
                            act_idx += act_cnt
        act_txt += ['};', '']
        evt_txt += ['};', '']
        map_txt += ['    %d' % tab_idx]
        map_txt += ['};', '']
        tab_txt += ['};', '']
        txt += act_txt
        txt += evt_txt
        txt += map_txt
        txt += tab_txt
        txt += ['']
        txt += ['static char *state_names[] = {', '    0,']
        for state in the_states:
            txt += ['    "%s",' % self.mkState(state)]
        txt += ['    0', '};', '']
        txt += ['static char *event_names[] = {', '    0,']
        for event in the_events:
            txt += ['    "%s",' % self.mkEvent(event)]
        txt += ['    0', '};', '']
        txt += ['static char *action_names[] = {', '    0,']
        for action in the_actions:
            txt += ['    "%s",' % self.mkAction(action)]
        txt += ['    0', '};', '']
        txt += ['']
        txt += ['static %s action_funcs[%s+1];' % (self.mkFunc('Action'), self.mkName('NUM_ACTIONS'))]
        txt += ['static %s classifier_funcs[%s+1];' % (self.mkFunc('Classify'), self.mkName('NUM_ACTIONS'))]
        txt += ['']
        txt += ['fsmStateMachine fsm_%s = {' % self.name]
        txt += ['    .name="%s",' % self.name]
        txt += ['    .numStates=%s,' % self.mkName('NUM_STATES')]
        txt += ['    .numEvents=%s,' % self.mkName('NUM_EVENTS')]
        txt += ['    .numTrans=%s,' % self.mkName('NUM_TRANS')]
        txt += ['    .numActions=%s,' % self.mkName('NUM_ACTIONS')]
        txt += ['    .maxActions=%s,' % self.mkName('MAX_ACTIONS')]
        if 'Entry' in the_events:
            txt += ['    .entryEvent=%s,' % (self.mkEvent('Entry'))]
        if 'Exit' in the_events:
            txt += ['    .exitEvent=%s,' % (self.mkEvent('Exit'))]
        txt += ['    .mapTab=map_table,']
        txt += ['    .actTab=action_table,']
        txt += ['    .evtTab=event_table,']
        txt += ['    .stateNames=state_names,']
        txt += ['    .eventNames=event_names,']
        txt += ['    .actionNames=action_names,']
        txt += ['    .transTab=trans_table,']
        txt += ['    .actionTab=action_funcs']
        txt += ['};', '']
        txt += ['#ifdef UNIT_TEST']
        for action in the_actions:
            txt += ['static int %s_test(fsmInstance *smi, fsmState state, fsmEvent event) {' %action]
            if action in classifier_list:
                next_event = classifier_list[action][0]
                txt += ['    printf("State: %%-20s, Event: %%-20s, Action: %-20s, NextEvent: %s\\n", smi->fsm->stateNames[state], smi->fsm->eventNames[event]);' % (action, next_event)]
                txt += ['    return %s;' % self.mkEvent(next_event)]
            else:
                txt += ['    printf("State: %%-20s, Event: %%-20s, Action: %-20s\\n", smi->fsm->stateNames[state], smi->fsm->eventNames[event]);' % action]
                txt += ['    return 0;']
            txt += ['}', '']
        txt += ['static void register_%s_actions(void) {' % (self.name)]
        txt += ['    fsmStateMachine *fsm = &fsm_%s;' % (self.name)]
        for action in the_actions:
            txt += ['    fsmSetActionFunction(fsm, %s, %s_test);' % (self.mkAction(action), action)]
        txt += ['};', '']
        txt += ['static void test_%s_actions(void) {' % (self.name)]
        txt += ['    fsmStateMachine *fsm = &fsm_%s;' % (self.name)]
        txt += ['    fsmInstance smi = { .name="test", .fsm=fsm };']
        txt += ['    fsmState state;']
        txt += ['    fsmEvent event;']
        txt += ['    int idx;']
        txt += ['    register_%s_actions();' % (self.name), '']
        txt += ['    for (state = 1; state <= fsm->numStates; ++state)']
        txt += ['        for (event = 1; event <= fsm->numEvents; ++event)']
        txt += ['            for (idx = 0; idx < fsm->numTrans; ++idx) {']
        txt += ['                fsmTransTab *tab = &fsm->transTab[idx];']
        txt += ['                if (tab->si == state && tab->ei == event) {']
        txt += ['                    smi.currentState = state;']
        txt += ['                    fsmRunStateMachine(&smi, event);']
        txt += ['                    if (smi.currentState != state)']
        txt += ['                        printf("       %s ===> %s\\n", fsm->stateNames[state], fsm->stateNames[smi.currentState]);']
        txt += ['                }']
        txt += ['            }']
        for test in self.tests:
            print "Test::", test
            txt += ['    do {']
            txt += ['        smi.currentState = %s;' % test.tests[0]]
            for t in test.tests:
                if t in the_states:
                    txt += ['        if (smi.currentState != %s) {' % t]
                    txt += ['            printf("State is %%s but expected %s\\n", fsm->stateNames[smi.currentState]);' % t]
                    txt += ['            break;']
                    txt += ['        }']
                else:
                    txt += ['        fsmRunStateMachine(&smi, %s);' % t]
            txt += ['        printf("Test Passed: %s\\n");' % repr(test)]
            txt += ['    } while (0);']
        txt += ['};', '']
        txt += ['int main(int argc, char *argv[]) {']
        txt += ['    fsmPrintStateMachine(&fsm_%s);' % (self.name)]
        txt += ['    test_%s_actions();' % (self.name)]
        txt += ['};', '']
        txt += ['#endif /* UNIT_TEST */']
        return (hdr, txt)

if __name__ == "__main__":
    print Event("test")
    print Event("test", ['with', 'args'])
    print State("Idle")
    print Transition("Idle", "test", "none", "Error")
    print Classifier("Idle", "test", "classify_me", "sub_event")
    print StateMachine("fred")
    sm = StateMachine("fred")
    sm.addEvent(Event("fredEvent"))
    sm.addEvent(Event("billEvent"))
    sm.addState(State("fredState"))
    sm.addState(State("billState"))
    sm.addTransition(Transition("fredState", "billEvent", "do_something", "billState"))
    sm.addTransition(Transition("billState", "fredEvent", "do_something", "fredState"))
    sm.addTransition(Transition("billState", "fredEvent", "do_something", "fredState"))
    sm.addClassifier(Classifier("billState", "fredEvent", "do_decide", "nextEvent"))
    sm.printit()
