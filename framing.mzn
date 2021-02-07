enum platforms = {PF_1,PF_2,PF_3};
enum slip_detectors = {force, tactile, fused};

slip_detectors: active_slip_detector;

var platforms:selected_platform;

array [platforms] of set of int: available_platforms = [{1,10,200},{0,10,100},{0,5,350}];

constraint (active_slip_detector ==force) -> forall(i in platforms)(available_platforms[i][1] == 1 -> selected_platform = i);

constraint (active_slip_detector ==tactile) -> forall(i in platforms)(available_platforms[i][2] == 10 -> selected_platform = i);

constraint (active_slip_detector ==fused) -> forall(i in platforms)(available_platforms[i][3] >= 250 -> selected_platform = i);

solve satisfy;
