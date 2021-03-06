%Inbuilt header file
include "table.mzn";
include "alldifferent.mzn";


%Thresholds of properties
bool: force_sensor_presence;  
int: min_tactile_sensor_count; 
int: min_memory_fused;               
int: min_latency;
int: max_latency;
int: req_force_plfm_type;


set of PLATFORMS: platforms;


%Indices of feature of every platform
set of int: FEATURES = 1..6;
int: name=1;                                                              
int: force_sensor = 2;
int: tactile_sensor = 3;
int: memory_availability = 4; 
int: force_sensor_type = 5;
int: latency = 6;


%Number of platforms
int: n_platforms;
set of int:PLATFORMS = 1..n_platforms;

%Array of platforms and properties
array[PLATFORMS] of string: n;       
array[PLATFORMS,FEATURES] of int: dd;

%Memory available in a platform is a dynamic property and therefore varies with time
array[PLATFORMS] of int : curr_memory_availability;


%Name of the platforms
n = ["nvidia_force","amd_tactile","intel_fused","nxp_force","exynos_force"];



%Platform properties
dd =  [| 1,   1,   50, curr_memory_availability[1], 1, 10,   % PF1
       | 2,   0,  100, curr_memory_availability[2], 0, 100,  % PF2
       | 3,   0,   10, curr_memory_availability[3], 0, 1000, % PF3
       | 4,   1,    0, curr_memory_availability[4], 2, 10,   % PF4
       | 5,   1,    0, curr_memory_availability[5], 3, 10,|];% PF5

%Platforms to be assigned for every sensor
array[FEATURES] of var int: force_platform; 
array[FEATURES] of var int: tactile_platform;
array[FEATURES] of var int: fused_platform;  


%Constraint of platform names to be in the provided table
constraint force_platform[name] in platforms;  
constraint tactile_platform[name] in platforms;
constraint fused_platform[name] in platforms;  


%Constraint that the values to be assigned to platform names are available in the table
constraint table(force_platform, dd);  
constraint table(tactile_platform, dd);
constraint table(fused_platform, dd);  

%Technical constraints

constraint force_platform[force_sensor] == force_sensor_presence;       %R1
constraint tactile_platform[tactile_sensor] >= min_tactile_sensor_count;%R2
constraint fused_platform[memory_availability]>=min_memory_fused;       %R3
constraint fused_platform[latency] <= max_latency;                      %R4
constraint fused_platform[latency] >= min_latency;                      %R5
constraint force_platform[force_sensor_type] == req_force_plfm_type;    %R6

%Platforms assigned to every slip detector need to be unique
constraint alldifferent([force_platform[name],tactile_platform[name],fused_platform[name]]);

solve satisfy;

%Prints platform names
output["force_platform =",n[fix(force_platform[name])],"\n",
       "tactile_platform =",n[fix(tactile_platform[name])],"\n",
       "fused_platform = ",n[fix(fused_platform[name])],"\n"];

%Prints platform indices
output["force_platform_index =",show(force_platform[name]),"\n",
       "tactile_platform_index =",show(tactile_platform[name]),"\n",
       "fused_platform_index = ",show(fused_platform[name]),"\n"];
