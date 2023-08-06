##*DxfStructure Command help*

---
###*Available functions*

|Name|Description|
|-------|----------|
|`(1)Show commands `| Displays list of command waiting to be done|
|`(2)Check and save `| Executes commands|

###*Layer system used for defining command in dxf modelspace *

|Name|Description|
|-------|----------|
|`DS_COMMAND`|Command text definition|

###*Command text special colours*
|Colour||meaning|
|-------|-|----------|
|`1 (red)`| |- frozen command colour - will not be detected during processing|
|any other| |- active command waiting to be executed|

Please note that all command text after execution will be automatic frozen (changed to red).

###*Available command*

|Syntax||Description|
|-------||----------|
|`steel section IPE 300`|| Draws IPE 300 section shape at command text insert point. Any other section form available section-base could be used|
|`steel section IPE`|| Draws all IPE section shapes at command text insert point. Any other section group name form available section-base could be used|
|`steel bolt M24`|| Draws M24 size bolt shape. M10, M12, M16, M20, M24, M30 sizes available.