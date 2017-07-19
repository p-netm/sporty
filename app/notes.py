"""Further Considerations:
 1). speed seems to be ahuge factor here, look at you algorithms and optimise
    -> hizi vitu hufai kuwa unaambiwa bana inafaa kukujanga tu,
 2). graceful recovery, say if a network error happens the program should be a
    able to restatr from its last point of execution to save time, resources and money
 3). telegram bot api integration
 4). increased metric patterns analysis
 5). trivial write a proper format and logic for the reporting part
 6). acocunt for extra time and penalties in the retrieve scores function and maybe also consider adding a
     a count of the number of mutual matches that are taken into account
 7). tipsters with the best efficiencies - > i meant incorporating typersi into your search
 8). accounting for pattern streak"""


""" On the second point am trying to tose a round a few ideas on how this might be accomplished without incurring
extra extensive functionalities like say databases. the program shiukd be able to know which link ita analysed last and proceed frm
there for a single day. it should be able to tell if there has been such a stop in execution and if there was then it should
know where it was and where it happened. if not it should countinue in the normal pattern of usage and once it stops before
the end of the webpage it should be able to record the final point of its execution.
t
first idea was using a single rewritable text file that records the link number currently recording as well as a timestamp



So far; we have functionalities that enable me to collect a matches scores as well as the scores of the mutual matches
Now i need an implementation that will save the state of match based on certain flags and then track a single team's
performance over the course of the next few matches that the said team will partake in. once a team is selected through
this procedure , it is stored or marked such that during the next occurrence the marked flag will signal that the team
could offer a better bet the objectives of the system should be such as pick a team on a any type of streak based on the
team's recent performance. Also the two teams in a match will be compared on the same basisi and should some certain
flags correspond such as say, one team is on a winning streak and the other is on a loss streak. the biggest challenge
that i think i currently face is that these operations will be invoked when certain timestamps are achieved and i have
yet worked out the ins of the said process. Also, the second hurdle in my way is that i need the app to be hosted on a
hosting server and an implementation of the staking percentage. Now keeping in mind that this process should be fully
finished by the end of this week."""