# Teamwork Documentation
A defining achievement of our teamwork was the completing a large portion of the project well before the due date.  This was the result of clear planning, regular meetings, managing expectations and the strategies in place for resolving problems both seen and unseen. Considering this, the project has been a pleasant experience.

# Setup Strategies

## Setting deadlines
From the beginning of iteration three, it became apparent that due to commitments to other courses as well as to have enough time to test code and write documentation, the tentative deadline for our group had to be set close to a week in advance. This was unanimously agreed upon by all members as each person had other major assignments due close to the actual due date of this project. As such the dates were set to the 10th November for all major code and test writing to be complete, the 14th for all contributions to the documentation to be complete and the 16th for final submissions.  By modularising the agile approach to the project, we were able to meet deadlines and fix errors along the way. 

## Regular meetings and purposes
A major driving factor to members meeting deadlines and providing adequate support to members who were struggling was the regular meetings that we had in place.  We were scheduled to meet three times a week, once over an online voice chat and twice in person. We shifted from an asynchronous setup to mitigate the issues of disjointed correspondence especially in view of tighter deadlines and to improve communication with all members of the team. Having meetings this regularly gave the group ample opportunity to collaborate effectively.

### Sunday
On Sundays the online voice chat discussion was scheduled. This meeting served two purposes. Firstly, to update the group on what had been accomplished over the weekend, this was quite helpful as it created arbitrary but useful deadlines which had to be met, less the member confess to the whole group as to why their section had not been reasonably attempted. Secondly, the meeting was used to outline major tasks that needed to be done and identifying sections of code that had errors or bugs. 
### Tuesday
On Tuesday an in-person meeting was scheduled, generally over lunch or coffee. The goal of this meeting was to code review sections which members had issues with or had no clue as to how to implement.  The meeting was set two days after as it gives members opportunity to identify any problems that they encounter.  This meeting was also used to give updates on a member's progress if the Sunday meeting went overtime or if there were any significant developments that occurred in the interim of two days. 
### Thursday  
On Thursday was the groups dedicated peer programming day, this was especially easy as we were all together with access to computers in the lab. After attempting the code assigned on the Sunday, Thursday was an appropriate time to ask tutors or more experienced members how the code worked or how to debug that section of code and was overall an enriching learning experience for all members.

## Meeting measures
In order to justify the frequencies of our meetings, we had to ensure that each meeting was meaningful and pushed the project forward. When considering our meetings from iteration one and two, the meetings were not as efficiently run as they could have been. This was especially true with online meetings where a lot of time was wasted due to misunderstandings.  

### Runsheet
A strategy used to ensure the high quality of our meetings was to come up with an agenda before the meeting. These points encompassed anything unclear in the group chat, the items predetermined for that day (see above for meeting purposes) and any items that required whole group consideration.  These points were written in dot point form on someone's phone or in a checklist.  This ensured we always knew what to talk about next and did not waste our time.
### Presenter style meeting (shared screen)
A large issue with online voice discussions was the inability to communicate complex ideas by talking alone.  By using the application discord, we were able to share screen which allowed us to represent ideas in drawings or directly show others their code.  This was especially useful in the discussions of git lab merge protocols and urgent code reviews. 
### Minute taking
Good minute taking was quintessential in our ability to communicate. It provided flexibility in that we were able to start meetings without everyone present (which ensured we did not waste time) and we were able to look back on details that were missed. This was especially useful for remembering our assigned to do list for the week.  The minutes were taken in dot point form and either had an individual's name as a tag or the points were encapsulated in the person's name as a heading. 

## Table of meeting dates and outcome summary
**Disclaimer** The following table is a summary of our meetings which required minutes. This does not encompass peer programming or code review sessions.

|**Date**|**Outcomes**|
|:---:|:-------|
|29 Oct| - Determined frequencies of meetings|
|| - Established git naming protocols  in style guide|
|| - Established git merge protocol -> thumbs up required|
|| - Pylint used for finding syntax errors|
|03 Nov| - Set 10th Nov as the code deadline| 
|| - Set goals to improve pylint and coverage to as close to 100% as possible|
||-	Setup google doc to contribute to documentation|
||-	Assigned people to compile documentation|
|05 Nov| - Discussed removal of wildcards|
|| - Emphasised task board|
|| - Decision to use decorators|
|| - Decision to remain with pickle|
|| - Coverage details|
|10 Nov| - Review of everyone's code|
||-	Discussion on removal of pylint error tag from consideration|
||-	 Assigned compiling of documentation|
|12 Nov|	-	Mass refactoring of redundant naming conventions|
||-	Removed misc.py and added standup.py. Relocated unrelated functions|
||-	Demo practice next week|
||-	Fixing timing of stand up|

# Further strategies

## Code Style
Carrying over from the last iteration, a key component of our ability to work in and as a team was the style guide outlined in our submission, "style_guide.md". By regulating the way code was written and naming variables, it made the code much easier to read when performing code reviews and much easier to write when peer programming or working on other people's code.  

## Branching and merging protocols
A section that was particularly fundamental in our groups ability to work together in this iteration was the branching protocols that we had in place.  If a section was being written by a member and they required help, another member would branch off the authors branch and only merge into the authors branch.  If the helper merged into the master branch, then the number of merge conflicts that would have to be sorted would be much greater than merging directly into the authors branch. This was inspired by the DRY principle to make working together more efficient. Further details of actual protocols are outlined in "style_guide.md"

## Peer programming
Peer programming was found to be a useful method to prevent a 'tunnel vision' approach to the project, resolve issues in our code and complete whole group task that needed to be done at the same time. It was also useful to directly show examples of how the code should or could be run in the time assigned which consolidated the approaches we would take when writing the code by ourselves.  A major example of this was the changing of naming conventions as the new requirements for no wildcard imports directly affected the whole groups code. By changing the naming convention from "channel.channel_create" to "channel.create", we removed redundant code to be more concise. However, it was recognised that if one person changed their code to this convention while the others lagged in doing so, we would not be able to work on the code in the meantime as no one would be able to run any of the test. By doing this in a peer programming setting, it was easy to rectify any errors in the change and it ensured that all members would be able to continue testing without any lag.

## Test protocols
One of our goals for this iteration was to bring coverage to 100% where possible. In order to do so it was necessary to systematically rewrite tests to include for all edge cases and general cases. We accomplished this by necessitating that each function have zero, single and many cases, any general cases applicable to the function as well as a test for each Value or Access error raised. By systematically approaching testings, it was quite easy to raise the coverage to 95% and then we were able to identify specific general cases that were not accounted for. We also specified that each test be refactored into separate functions rather than encompassing them in large function blocks.  While this did create a lot more setups for each function, it became much easier to identify which sections of the code do not work and which test do.  By applying a systematic, scientific approach we were able to achieve a coverage score quite close to 100%.

# Challenges
## Other commitments
Like in all group projects every member had other commitments in other courses, work and family. Being able to communicate these commitments and helping each other work around this is crucial to the completion of the project.  The deadlines set for us, reflected the various assignments due at different times. While it is not optimal to work on multiple projects at the same time, having the system of support within the team way a key factor in our ability to complete the project. The protocols and strategies that we have in place is a product of learning to work with each other through the past two iterations.   

## Data storage -> JSON vs Pickle
A significant amount of thought went into the decision of using JSON or pickle to store data. After iteration 2 we had ended up with pickle as we had thought time fields had to be stored as datatime objects which couldn't be stored by JSON. Once we found that this was not the case, we discussed using JSON due to the readability and debugging of the code however we ran into issues with keys being converted to strings so once returned, broke our code. Eventually it was decided to return to pickle. Having these back and forth discussions over an extended period was solely facilitated by our frequency and quality of meetings.  Through these meetings we were able to come to a consensus as a team. 

## Code reliance on other people 
An issue commonly run into in coding projects are code dependencies.  This can be quite precarious as any code which does not match the updated specification and code which has systemic bugs may cause the whole project to crash. This was addressed in the previous iterations but at the beginning of iteration three we wished to improve the process.  Our solution was to set priorities to the tasks, considering the dependencies of task on another and set deadlines on the task.  Having regular meetings kept members accountable to the deadlines and ensured set amounts of work was done at a given time. The iterative style of approaching the project improved group efficiency and productivity. 

## Refactoring and reaching consensus
A major group decision was to decide to refactor the naming of all functions and function calls to be more concise. However, one member also addressed that this could be redundant and could possibly cause issues within our code. Without a whole group consensus, we could not proceed and therefore we applied our previous conflict resolution strategy. Each member could either side with one argument, present an alternative or remain indifferent. If no consensus was reached, then the opposing sides would further present their arguments. It was only when the whole group came to a consensus would we proceed. 

## Circular imports & removal of misc.py
As a product of modularising the whole project from iteration one, circular imports became an issue in this iteration.  This was where message.py imported standup functions and standup.py imported message functions. After identifying this issue, circular imports were addressed in the subsequent meeting. Since it was a problem which impacted on the overall design efficiency of the project, the team reached a consensus to completely remove the misc.py and redistribute the other functions to appropriate files. By merging functionalities, the project was appropriately streamlined.
 
## Documention conception example
The following link is an example of how documentation was conceived within the team. Each member would contribute on the major points listed in the specifications and a single member would compile the document to ensure that the documentation had an appropriate flow and progression.  While the example below is for teamwork, similar processes had been carried out for SE principles.   

[https://docs.google.com/document/d/1cHGlNayvvgBAc_jkH0gJWPBBw9DJlH04gw_M6bNTtTM/edit]

