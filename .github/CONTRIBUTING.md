# Contributing to the Portal Modelo Ombudsman 

If you would like to contribute to the project, it may be a good idea to start by [README](https://github.com/interlegis/interlegis.portalmodelo.ombudsman/blob/master/README.rst) to get to know us better.

Thanks for contributing!  :+1:


## How could I contribute?

### Reporting a Bug

* If the bug found is not in the _Issues_, just open a [New _Issue_](https://github.com/interlegis/interlegis.portalmodelo.ombudsman/issues/new)

### Adding and / or modifying some functionality

* First check that there is no [_Issue_](https://github.com/interlegis/interlegis.portalmodelo.ombudsman/issues) regarding this modification and / or addition.

* If it does not exist, create a [New _Issue_](https://github.com/interlegis/interlegis.portalmodelo.ombudsman/issues/new). Give a meaningful title to it, put a description and at least a _label_.

* Changes must be submitted through [_Pull Requests_](https://github.com/interlegis/interlegis.portalmodelo.ombudsman/issues/new/compare).


## _Commit_ pattern

#### For standardization issues we recommend following our _commit_ style:

* _Commits_ should all be in __english__;

* It should contain a short and objective title of what was done in that _commit_;

* After this title, one should describe, with a little more detail, all the activities performed.

* If you are working with an associate sign on your _commits_ your partners

__Example:__

Creating project community files (Short title and objective)

    Adds project license (Description of one of the activities)

    Adds project code of conduct file

    Adds project contributing file

    Adds project issue template file

    Adds projects pull request file

    Co-authored-by: user.name <user.email@example.com> (partnership signature)

## _Branchs_ policy

With the goal of maintaining the completeness and reliability of the project code, the use of branch policy was proposed.
This Branches Policy should guide developers in organizing their contributions to the repository.
__OBS__: The _branchs_ policy was designed to work in conjunction with the _git flow_ tool, its documentation and more information can be accessed [here](https://github.com/nvie/gitflow).

* __develop__ - Main branch of the repository where only consolidated and tested software integration will be allowed. This branch will be exclusively for the delivery of Realeases, that is, a greater set of functionalities that integrate the software, here will be the version _ ** stable ** _ of the software.

* __develop__ - Branch for integration of new functionalities, where it will be allowed the delivery of the features developed and that are in an advanced stage of completeness. It will be the base branch for the beginning of the development of the features and of the correction of bugs. The releases will also be released here.

* __feature__ / <name-of-feature> __ - Branch used to develop new features of _backlog_. If the feature has been proposed by a _issue_ of the repository and accepted in _backlog_ the name should contain the _issue_ number.
Ex: feature / 1- <new-feature-name> (whereas feature has been requested in _issue_ # 1)

* __bugfix__ / <bug-name> __ - Branch used to fix low / medium urgency bugs that are not present in the __develop__ branch. If the bug has been reported by a _issue_ from the repository the name should contain the _issue_ number.
 Ex: bugfix / 1- <bug-description> (whereas bug has been reported in _issue_ # 1)

* __hotfix__ / <bug-name> __ - Branch used to fix high-urgency bugs that are present in the __develop__ branch. If the bug has been reported by a _issue_ from the repository the name should contain the _issue_ number.
 Ex: bugfix / 1- <bug-description> (whereas bug has been reported in _issue_ # 1)

* __release__ / <release-version> __ - Branch where the final / build adjustments will be made before delivery of a software product version. Branch name will be the version of the release to be delivered.

* __support__ / <theme-or-nature> __ - Branch where support tasks related to the software will be executed, such as documentation development, configuration management nature corrections and so on.

