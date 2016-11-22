#ifndef _SALARY_H
#define _SALARY_H_
#include "common.h"

typedef enum {
    QingWen = 0,
    SheYue,
    XiRen,
    MaxStaffNum
}staffType;

typedef enum {
    JiaBaoyu = 0,
    JiaMu,
    WangFuren,
    JiaZheng,
    MaxBossNum
}bossType;
typedef enum {
    Jan = 0,
    Feb,
    Mar,
    Apr,
    May,
    Jun,
    Jul,
    Aug,
    Sep,
    Oct,
    Nov,
    Dec,
    MaxMonthNum
}monthType;

typedef SWORD32 salaryType;
#define INVALID_SALARY ((salaryType)0x80000000)

extern salaryType calcSalary(bossType boss, staffType staff, monthType month);

#endif


