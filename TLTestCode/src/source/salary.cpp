#include "salary.h"

typedef salaryType (*calcStaffFixSalaryFactor)(monthType month);
typedef salaryType (*calcStaffRewardFactor)(monthType month);
typedef salaryType (*calcBossSalaryFactor)(salaryType staffFixSalary, salaryType staffRewardFactor);

#define isOddMonth(month) (0 == ((month) & 0x01))
salaryType calcQingWenFixSalaryFactor(monthType month)
{
    return isOddMonth(month)?900:800;
}
salaryType calcQingWenRewardFactor(monthType month)
{
    return 500;
}
salaryType calcSheYueFixSalaryFactor(monthType month)
{
    return 600;
}
#define isFirstHalfYear(month) ((month) <= Jun)
salaryType calcSheYueRewardFactor(monthType month)
{
    return isFirstHalfYear(month)?400:700;
}
#define getSeason(month) (((month)/3)+1)
#define isOdd(in) ((in)&0x01)
salaryType calcXiRenFixSalaryFactor(monthType month)
{
    return isOdd(getSeason(month))?1000:1500;
}
salaryType calcXiRenRewardFactor(monthType month)
{
    return 2000;
}
calcStaffFixSalaryFactor fcalcStaffFixSalaryFactor[MaxStaffNum] = { calcQingWenFixSalaryFactor,
                                                                    calcSheYueFixSalaryFactor,
                                                                    calcXiRenFixSalaryFactor
                                                                  };
calcStaffRewardFactor fcalcStaffRewardFactor[MaxStaffNum] = {   calcQingWenRewardFactor,
                                                                calcSheYueRewardFactor,
                                                                calcXiRenRewardFactor
                                                            };
salaryType calcJiaBaoyuSalary(salaryType staffFixSalary, salaryType staffRewardFactor)
{
    return (staffFixSalary + staffRewardFactor)<<3;
}
#define getMax(a,b) (((a) >= (b))?(a):(b))
#define getMin(a,b) (((a) <= (b))?(a):(b))
salaryType calcJiaMuSalary(salaryType staffFixSalary, salaryType staffRewardFactor)
{
    return getMax(staffFixSalary, staffRewardFactor) * 10;
}
salaryType calcWangFurenSalary(salaryType staffFixSalary, salaryType staffRewardFactor)
{
    return getMin(staffFixSalary, staffRewardFactor) * 5;
}
salaryType calcJiaZhengSalary(salaryType staffFixSalary, salaryType staffRewardFactor)
{
    return staffFixSalary * 4 + staffRewardFactor * 2;
}

calcBossSalaryFactor fcalcBossSalaryFactor[MaxBossNum] = {  calcJiaBaoyuSalary,
                                                            calcJiaMuSalary,
                                                            calcWangFurenSalary,
                                                            calcJiaZhengSalary
                                                         };
salaryType calcSalary(bossType boss, staffType staff, monthType month)
{
    salaryType FixSalary = 0;
    salaryType Reward = 0;

    CHECK(boss < MaxBossNum, return INVALID_SALARY);
    CHECK(staff < MaxStaffNum, return INVALID_SALARY);
    CHECK(month < MaxMonthNum, return INVALID_SALARY);
    
    FixSalary = (*fcalcStaffFixSalaryFactor[staff])(month);
    Reward = (*fcalcStaffRewardFactor[staff])(month);

    return (*fcalcBossSalaryFactor[boss])(FixSalary, Reward);
}



