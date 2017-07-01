"""Further Considerations:
 1). speed seems to be ahuge factor here, look at you algorithms and optimise
    -> hizi vitu hufai kuwa unaambiwa bana inafaa kukujanga tu,
 2). graceful recovery, say if a network error happens the program should be a
    able to restatr from its last point of execution to save time, resources and money
 3). telegram bot api integration
 4). increased metric patterns analysis
 5). trivial write a proper format and logic for the reporting part"""


""" On the second point am trying to tose a round a few ideas on how this might be accomplished without incurring
extra extensive functionalities like say databases. the program shiukd be able to know which link ita analysed last and proceed frm
there for a single day. it should be able to tell if there has been such a stop in execution and if there was then it should
know where it was and where it happened. if not it should countinue in the normal pattern of usage and once it stops before
the end of the webpage it should be able to record the final point of its execution.
t
first idea was using a single rewritable text file that records the link number currently recording as well as a timestamp"""