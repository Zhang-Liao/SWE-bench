# pvlib__pvlib-python-980

## 基本信息

- **实例ID**: pvlib__pvlib-python-980
- **仓库**: pvlib/pvlib-python
- **版本**: 0.7
- **创建时间**: 2020-06-12T17:45:46Z
- **基础提交**: 75369dcabacb6c6c38790cc23825f33f155ad1a9
- **环境设置提交**: 6e5148f59c5050e8f7a0084b7ae39e93b80f72e6

## 问题描述

pvlib.soiling.hsu model implementation errors
**Describe the bug**
I ran an example run using the Matlab version of the HSU soiling function and found that the python version did not give anywhere near the same results.  The Matlab results matched the results in the original JPV paper.  As a result of this test, I found two errors in the python implementation, which are listed below:

1.  depo_veloc = {'2_5': 0.004, '10': 0.0009} has the wrong default values.  They are reversed.
The proper dictionary should be: {'2_5': 0.0009, '10': 0.004}.  This is confirmed in the JPV paper and the Matlab version of the function.

2. The horiz_mass_rate is in g/(m^2*hr) but should be in g/(m^2*s).  The line needs to be multiplied by 60x60 or 3600.
The proper line of code should be: 
horiz_mass_rate = (pm2_5 * depo_veloc['2_5']+ np.maximum(pm10 - pm2_5, 0.) * depo_veloc['10'])*3600

When I made these changes I was able to match the validation dataset from the JPV paper, as shown below.
![image](https://user-images.githubusercontent.com/5392756/82380831-61c43d80-99e6-11ea-9ee3-2368fa71e580.png)




## 解决方案补丁


```diff
diff --git a/pvlib/soiling.py b/pvlib/soiling.py
--- a/pvlib/soiling.py
+++ b/pvlib/soiling.py
@@ -12,8 +12,8 @@
 def hsu(rainfall, cleaning_threshold, tilt, pm2_5, pm10,
         depo_veloc=None, rain_accum_period=pd.Timedelta('1h')):
     """
-    Calculates soiling ratio given particulate and rain data using the model
-    from Humboldt State University (HSU).
+    Calculates soiling ratio given particulate and rain data using the
+    Fixed Velocity model from Humboldt State University (HSU).
 
     The HSU soiling model [1]_ returns the soiling ratio, a value between zero
     and one which is equivalent to (1 - transmission loss). Therefore a soiling
@@ -76,8 +76,17 @@ def hsu(rainfall, cleaning_threshold, tilt, pm2_5, pm10,
     # cleaning is True for intervals with rainfall greater than threshold
     cleaning_times = accum_rain.index[accum_rain >= cleaning_threshold]
 
-    horiz_mass_rate = pm2_5 * depo_veloc['2_5']\
-        + np.maximum(pm10 - pm2_5, 0.) * depo_veloc['10'] * 3600
+    # determine the time intervals in seconds (dt_sec)
+    dt = rainfall.index
+    # subtract shifted values from original and convert to seconds
+    dt_diff = (dt[1:] - dt[:-1]).total_seconds()
+    # ensure same number of elements in the array, assuming that the interval
+    # prior to the first value is equal in length to the first interval
+    dt_sec = np.append(dt_diff[0], dt_diff).astype('float64')
+
+    horiz_mass_rate = (
+        pm2_5 * depo_veloc['2_5'] + np.maximum(pm10 - pm2_5, 0.)
+        * depo_veloc['10']) * dt_sec
     tilted_mass_rate = horiz_mass_rate * cosd(tilt)  # assuming no rain
 
     # tms -> tilt_mass_rate

```

## spec
不知道怎么处理，无法通过图像找到output

```py

def test(rainfall_input)
    depo_veloc = {'2_5': 1.0e-4, '10': 1.0e-4}
    rain = pd.DataFrame(data=rainfall_input)
    # define time deltas in minutes
    timedelta = [0, 0, 0, 0, 0, 30, 0, 30, 0, 30, 0, -30,
    -30, -30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    rain['mins_added'] = pd.to_timedelta(timedelta, 'm')
    rain['new_time'] = rain.index + rain['mins_added']
    rain_var_times = rain.set_index('new_time').iloc[:, 0]
    result = hsu(
        rainfall=rain_var_times, cleaning_threshold=0.5, tilt=50.0,
        pm2_5=1, pm10=2, depo_veloc=depo_veloc,
        rain_accum_period=pd.Timedelta('2h'))
    return result
```
<!-- assert np.allclose(result, expected_output_3) -->

## 测试补丁

```diff
diff --git a/pvlib/tests/test_soiling.py b/pvlib/tests/test_soiling.py
--- a/pvlib/tests/test_soiling.py
+++ b/pvlib/tests/test_soiling.py
@@ -18,24 +18,24 @@ def expected_output():
                        end=pd.Timestamp(2019, 1, 1, 23, 59, 0), freq='1h')
 
     expected_no_cleaning = pd.Series(
-        data=[0.97230454, 0.95036146, 0.93039061, 0.91177978, 0.89427556,
-              0.8777455 , 0.86211038, 0.84731759, 0.83332881, 0.82011354,
-              0.80764549, 0.79590056, 0.78485556, 0.77448749, 0.76477312,
-              0.75568883, 0.74721046, 0.73931338, 0.73197253, 0.72516253,
-              0.7188578 , 0.71303268, 0.7076616 , 0.70271919],
+        data=[0.96998483, 0.94623958, 0.92468139, 0.90465654, 0.88589707,
+              0.86826366, 0.85167258, 0.83606715, 0.82140458, 0.80764919,
+              0.79476875, 0.78273241, 0.77150951, 0.76106905, 0.75137932,
+              0.74240789, 0.73412165, 0.72648695, 0.71946981, 0.7130361,
+              0.70715176, 0.70178307, 0.69689677, 0.69246034],
         index=dt)
     return expected_no_cleaning
 
 @pytest.fixture
 def expected_output_1():
     dt = pd.date_range(start=pd.Timestamp(2019, 1, 1, 0, 0, 0),
-        end=pd.Timestamp(2019, 1, 1, 23, 59, 0), freq='1h')
+                       end=pd.Timestamp(2019, 1, 1, 23, 59, 0), freq='1h')
     expected_output_1 = pd.Series(
-        data=[0.9872406 , 0.97706269, 0.96769693, 0.95884032, 1.,
-              0.9872406 , 0.97706269, 0.96769693, 1.        , 1.        ,
-              0.9872406 , 0.97706269, 0.96769693, 0.95884032, 0.95036001,
-              0.94218263, 0.93426236, 0.92656836, 0.91907873, 0.91177728,
-              0.9046517 , 0.89769238, 0.89089165, 0.88424329],
+        data=[0.98484972, 0.97277367, 0.96167471, 0.95119603, 1.,
+              0.98484972, 0.97277367, 0.96167471, 1., 1.,
+              0.98484972, 0.97277367, 0.96167471, 0.95119603, 0.94118234,
+              0.93154854, 0.922242, 0.91322759, 0.90448058, 0.89598283,
+              0.88772062, 0.87968325, 0.8718622, 0.86425049],
         index=dt)
     return expected_output_1
 
@@ -44,15 +44,31 @@ def expected_output_2():
     dt = pd.date_range(start=pd.Timestamp(2019, 1, 1, 0, 0, 0),
                        end=pd.Timestamp(2019, 1, 1, 23, 59, 0), freq='1h')
     expected_output_2 = pd.Series(
-        data=[0.97229869, 0.95035106, 0.93037619, 0.91176175, 1.,
-              1.        , 1.        , 0.97229869, 1.        , 1.        ,
-              1.        , 1.        , 0.97229869, 0.95035106, 0.93037619,
-              0.91176175, 0.89425431, 1.        , 1.        , 1.        ,
-              1.        , 0.97229869, 0.95035106, 0.93037619],
+        data=[0.95036261, 0.91178179, 0.87774818, 0.84732079, 1.,
+              1., 1., 0.95036261, 1., 1.,
+              1., 1., 0.95036261, 0.91178179, 0.87774818,
+              0.84732079, 0.8201171, 1., 1., 1.,
+              1., 0.95036261, 0.91178179, 0.87774818],
         index=dt)
-
     return expected_output_2
 
+
+@pytest.fixture
+def expected_output_3():
+    dt = pd.date_range(start=pd.Timestamp(2019, 1, 1, 0, 0, 0),
+                       end=pd.Timestamp(2019, 1, 1, 23, 59, 0), freq='1h')
+    timedelta = [0, 0, 0, 0, 0, 30, 0, 30, 0, 30, 0, -30,
+                 -30, -30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
+    dt_new = dt + pd.to_timedelta(timedelta, 'm')
+    expected_output_3 = pd.Series(
+        data=[0.96576705, 0.9387675, 0.91437615, 0.89186852, 1.,
+              1., 0.98093819, 0.9387675, 1., 1.,
+              1., 1., 0.96576705, 0.9387675, 0.90291005,
+              0.88122293, 0.86104089, 1., 1., 1.,
+              0.96576705, 0.9387675, 0.91437615, 0.89186852],
+        index=dt_new)
+    return expected_output_3
+
 @pytest.fixture
 def rainfall_input():
 
@@ -105,12 +121,30 @@ def test_hsu_defaults(rainfall_input, expected_output_1):
     Test Soiling HSU function with default deposition velocity and default rain
     accumulation period.
     """
-    result = hsu(
-        rainfall=rainfall_input, cleaning_threshold=0.5, tilt=0.0,
-        pm2_5=1.0e-2,pm10=2.0e-2)
+    result = hsu(rainfall=rainfall_input, cleaning_threshold=0.5, tilt=0.0,
+                 pm2_5=1.0e-2, pm10=2.0e-2)
     assert np.allclose(result.values, expected_output_1)
 
 
+@requires_scipy
+def test_hsu_variable_time_intervals(rainfall_input, expected_output_3):
+    """
+    Test Soiling HSU function with variable time intervals.
+    """
+    depo_veloc = {'2_5': 1.0e-4, '10': 1.0e-4}
+    rain = pd.DataFrame(data=rainfall_input)
+    # define time deltas in minutes
+    timedelta = [0, 0, 0, 0, 0, 30, 0, 30, 0, 30, 0, -30,
+                 -30, -30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
+    rain['mins_added'] = pd.to_timedelta(timedelta, 'm')
+    rain['new_time'] = rain.index + rain['mins_added']
+    rain_var_times = rain.set_index('new_time').iloc[:, 0]
+    result = hsu(
+        rainfall=rain_var_times, cleaning_threshold=0.5, tilt=50.0,
+        pm2_5=1, pm10=2, depo_veloc=depo_veloc,
+        rain_accum_period=pd.Timedelta('2h'))
+    assert np.allclose(result, expected_output_3)
+
 @pytest.fixture
 def greensboro_rain():
     # get TMY3 data with rain

```

## 测试信息

### 失败的测试 (FAIL_TO_PASS)
["pvlib/tests/test_soiling.py::test_hsu_no_cleaning", "pvlib/tests/test_soiling.py::test_hsu", "pvlib/tests/test_soiling.py::test_hsu_defaults", "pvlib/tests/test_soiling.py::test_hsu_variable_time_intervals"]

### 通过的测试 (PASS_TO_PASS)
["pvlib/tests/test_soiling.py::test_kimber_nowash", "pvlib/tests/test_soiling.py::test_kimber_manwash", "pvlib/tests/test_soiling.py::test_kimber_norain", "pvlib/tests/test_soiling.py::test_kimber_initial_soil"]

## 提示信息

nice sleuthing Josh! Is a PR forthcoming? 🎉 
Hi Mark,
                Yes, a PR is in the works.  I need to improve the testing first.

-Josh

From: Mark Mikofski <notifications@github.com>
Reply-To: pvlib/pvlib-python <reply@reply.github.com>
Date: Tuesday, May 19, 2020 at 3:51 PM
To: pvlib/pvlib-python <pvlib-python@noreply.github.com>
Cc: Joshua Stein <jsstein@sandia.gov>, Author <author@noreply.github.com>
Subject: [EXTERNAL] Re: [pvlib/pvlib-python] pvlib.soiling.hsu model implementation errors (#970)


nice sleuthing Josh! Is a PR forthcoming? 🎉

—
You are receiving this because you authored the thread.
Reply to this email directly, view it on GitHub<https://github.com/pvlib/pvlib-python/issues/970#issuecomment-631102921>, or unsubscribe<https://github.com/notifications/unsubscribe-auth/ABJES5C2CRTZFF7ROT2EPOTRSL5ORANCNFSM4NFL4K3Q>.

Now I need to go back and figure out where I missed these errors in the review.

---

*此文件由SWE-bench数据自动生成*
*生成时间: 2025-10-20 11:39:41*
