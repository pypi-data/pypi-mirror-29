#include <TH/TH.h>

#define cluster_(NAME) TH_CONCAT_4(cluster_, NAME, _, Real)

#include "generic/cpu.c"
#include "THGenerateAllTypes.h"
