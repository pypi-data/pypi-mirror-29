from mythril.analysis.report import Issue
import re
import logging


'''
MODULE DESCRIPTION:

Check for constraints on tx.origin (i.e., access to some functionality is restricted to a specific origin).
'''

def execute(statespace):

    logging.debug("Executing module: DEPRECIATED OPCODES")

    issues = []

    for k in statespace.nodes:
        node = statespace.nodes[k]

        for instruction in node.instruction_list:

            if(instruction['opcode'] == "ORIGIN"):

                issue = Issue(node.module_name, node.function_name, None,  "Use of tx.origin", "Warning", \
                    "Function " + node.function_name + " retrieves the transaction origin (tx.origin) using the ORIGIN opcode. Use tx.sender instead.\nSee also: https://solidity.readthedocs.io/en/develop/security-considerations.html#tx-origin"
                )
                
                issues.append(issue)
    
    return issues
