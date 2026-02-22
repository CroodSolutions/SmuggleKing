# SmuggleKing

## Testing Methodology Overview

This testing framework and toolset, is speicific to evaluating ways to test the effectiveness of Isolation Browsers and download restrictions policies of kiosks. The primary tool and technique associated with this is a carefully-crafted web page setup with LotL binaries (kiosk) or custom payload for adversary emulation of ClickFix style attacks. This project will provide what you need to setup such a page in [Section 3](https://github.com/CroodSolutions/SmuggleKing/tree/main/3%20-%20SmuggleKing%20Application) of this repo to get you started, although we expect testers and researchers will adapt and customize versions of this based upon their own needs. 

## Proposed Testing Procedures for Isolation Browsers
(under construction)

## Testing Procedures for Kiosks

The testing procedures for kiosks are the same as for isolation browsers, with two exceptions:

 - ClickFix style Social Engineering elements are no longer necessarily or valuable to test, because kiosk hacking starts with the assumption that the attacker has physical access to the kiosk.
 - For Kiosk Hacking, these tests usually need to be combined with other kiosk escape tactics, to get to both a somewhat unlocked browser that allows for input of an attacker-controlled URL, as well as some file dialog box access (e.g., File Open) to actually run the smuggled payload.  

For the more detailed topic of Kiosk Hacking and Security, check out our other project [CTRL+ESC+HOST](https://github.com/CroodSolutions/CTRL-ESC-HOST/tree/main).

 ## Legal and Ethical Notice

Only test on your own isolation browser instances or kiosks and/or with proper written permission and following all appropriate industry ethics and best practices, such as within the scope of a penetration test or bug bounty program.  
 
