% software_components: 1 -> force slip, 2 -> tactile slip, 3 -> fused
int: stationary;
int: gripper_value;
var 0..1:force_slip_detector; var 0..1: tactile_slip_detector; var 0..1: fused_slip_detector;  
%var 0..1: force_sensor; var 0..6: tactile_sensor;  var 1..1000: memory_capacity;   

%constraint if gripper_value == 1 then gripper_open = 1 else gripper_closed = 0 endif;
%gripper_value = 1 -> gripper_closed, gripper_value = 0 -> gripper_open 
constraint ((stationary == 1) /\ (gripper_value == 0)) -> force_slip_detector = 0;
constraint ((stationary == 1) /\ (gripper_value == 0)) -> tactile_slip_detector = 1;

constraint ((stationary == 1) /\ (gripper_value == 1)) -> force_slip_detector = 1;
constraint ((stationary == 1) /\ (gripper_value == 1)) -> tactile_slip_detector = 0;

constraint (stationary == 0)-> fused_slip_detector == 1;

%constraint ((stationary == 1) /\ (gripper_value == 0)) -> force_sensor = 0;
%constraint ((stationary == 1) /\ (gripper_value == 0)) -> tactile_sensor > 1;
%constraint ((stationary == 1) /\ (gripper_value == 0)) -> memory_capacity < 250;

%constraint ((stationary == 1) /\ (gripper_value == 1))-> force_sensor = 1;
%constraint ((stationary == 1) /\ (gripper_value == 1)) -> tactile_sensor = 0;
%constraint ((stationary == 1) /\ (gripper_value == 1)) -> memory_capacity > 250;

%constraint (stationary == 0)-> force_sensor = 1;
%constraint (stationary == 0)-> tactile_sensor > 1;
%constraint (stationary == 0)-> memory_capacity > 250;

solve satisfy;

