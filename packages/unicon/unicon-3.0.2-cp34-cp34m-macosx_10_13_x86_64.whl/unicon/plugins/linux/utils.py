import re

from unicon.utils import Utils, AttributeDict

class LinuxUtils(Utils):

    def truncate_trailing_prompt(self, pattern, result, hostname=None):
        # Prompt pattern syntax is different from the generic plugin
        # The regex group match is grouped around the prompt itself
        match = re.findall(pattern, result, re.MULTILINE)
        if match:
             # get the last prompt pattern match line and replace it with ""
             prompt_line = match[-1][0]
             output = result.replace(prompt_line, "")
        else:
            output = result
        return output.strip()
