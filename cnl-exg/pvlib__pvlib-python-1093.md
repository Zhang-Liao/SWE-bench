# pvlib__pvlib-python-1093

## 基本信息

- **实例ID**: pvlib__pvlib-python-1093
- **仓库**: pvlib/pvlib-python
- **版本**: 0.7
- **创建时间**: 2020-11-20T22:36:43Z
- **基础提交**: 11c356f9a89fc88b4d3ff368ce1aae170a97ebd7
- **环境设置提交**: 6e5148f59c5050e8f7a0084b7ae39e93b80f72e6

## 问题描述

ModelChain.prepare_inputs can succeed with missing dhi
From the docstring for `ModelChain.prepare_inputs()` I believe the method should fail if `weather` does not have a `dhi` column.

The validation checks for `'ghi'` twice, but not `'dhi`'

https://github.com/pvlib/pvlib-python/blob/11c356f9a89fc88b4d3ff368ce1aae170a97ebd7/pvlib/modelchain.py#L1136


## 解决方案补丁

```diff
diff --git a/pvlib/modelchain.py b/pvlib/modelchain.py
--- a/pvlib/modelchain.py
+++ b/pvlib/modelchain.py
@@ -1133,7 +1133,7 @@ def prepare_inputs(self, weather):
         ModelChain.complete_irradiance
         """
 
-        self._verify_df(weather, required=['ghi', 'dni', 'ghi'])
+        self._verify_df(weather, required=['ghi', 'dni', 'dhi'])
         self._assign_weather(weather)
 
         self.times = self.weather.index

```

## spec


```py
# Precondition:
# The input arguments sapm_dc_snl_ac_system, location, missing are a used to for test in the test script.
# Weather is a dictionary with three fields.
# - filed 1 is dhi. It is a list of two integers.
# - filed 2 is dni. It is a list of two integers.
# - filed 3 is ghi. It is a list of two integers.
# Or weather is a dictionary with two fields.
# - filed 2 is dni. It is a list of two integers.
# - filed 3 is ghi. It is a list of two integers.

# Postcondition:
# If Weather has the field ghi, the function does not crush
# Else, the function raise an value error about weather
def test_prepare_inputs_missing_irrad_component(
        sapm_dc_snl_ac_system, location, missing, weather):
    mc = ModelChain(sapm_dc_snl_ac_system, location)
    weather.drop(columns=missing, inplace=True)
    with pytest.raises(ValueError):
        mc.prepare_inputs(weather)
```
## 测试补丁

```diff
diff --git a/pvlib/tests/test_modelchain.py b/pvlib/tests/test_modelchain.py
--- a/pvlib/tests/test_modelchain.py
+++ b/pvlib/tests/test_modelchain.py
@@ -249,6 +249,16 @@ def test_prepare_inputs_no_irradiance(sapm_dc_snl_ac_system, location):
         mc.prepare_inputs(weather)
 
 
+@pytest.mark.parametrize("missing", ['dhi', 'ghi', 'dni'])
+def test_prepare_inputs_missing_irrad_component(
+        sapm_dc_snl_ac_system, location, missing):
+    mc = ModelChain(sapm_dc_snl_ac_system, location)
+    weather = pd.DataFrame({'dhi': [1, 2], 'dni': [1, 2], 'ghi': [1, 2]})
+    weather.drop(columns=missing, inplace=True)
+    with pytest.raises(ValueError):
+        mc.prepare_inputs(weather)
+
+
 def test_run_model_perez(sapm_dc_snl_ac_system, location):
     mc = ModelChain(sapm_dc_snl_ac_system, location,
                     transposition_model='perez')

```

## 测试信息

### 失败的测试 (FAIL_TO_PASS)
["pvlib/tests/test_modelchain.py::test_prepare_inputs_missing_irrad_component[dhi]"]

### 通过的测试 (PASS_TO_PASS)
["pvlib/tests/test_modelchain.py::test_ModelChain_creation", "pvlib/tests/test_modelchain.py::test_with_sapm", "pvlib/tests/test_modelchain.py::test_with_pvwatts", "pvlib/tests/test_modelchain.py::test_orientation_strategy[None-expected0]", "pvlib/tests/test_modelchain.py::test_orientation_strategy[None-expected1]", "pvlib/tests/test_modelchain.py::test_orientation_strategy[flat-expected2]", "pvlib/tests/test_modelchain.py::test_orientation_strategy[south_at_latitude_tilt-expected3]", "pvlib/tests/test_modelchain.py::test_run_model_with_irradiance", "pvlib/tests/test_modelchain.py::test_prepare_inputs_no_irradiance", "pvlib/tests/test_modelchain.py::test_prepare_inputs_missing_irrad_component[ghi]", "pvlib/tests/test_modelchain.py::test_prepare_inputs_missing_irrad_component[dni]", "pvlib/tests/test_modelchain.py::test_run_model_perez", "pvlib/tests/test_modelchain.py::test_run_model_gueymard_perez", "pvlib/tests/test_modelchain.py::test_run_model_with_weather_sapm_temp", "pvlib/tests/test_modelchain.py::test_run_model_with_weather_pvsyst_temp", "pvlib/tests/test_modelchain.py::test_run_model_with_weather_faiman_temp", "pvlib/tests/test_modelchain.py::test_run_model_with_weather_fuentes_temp", "pvlib/tests/test_modelchain.py::test_run_model_tracker", "pvlib/tests/test_modelchain.py::test__assign_total_irrad", "pvlib/tests/test_modelchain.py::test_prepare_inputs_from_poa", "pvlib/tests/test_modelchain.py::test__prepare_temperature", "pvlib/tests/test_modelchain.py::test_run_model_from_poa", "pvlib/tests/test_modelchain.py::test_run_model_from_poa_tracking", "pvlib/tests/test_modelchain.py::test_run_model_from_effective_irradiance", "pvlib/tests/test_modelchain.py::test_infer_dc_model[sapm]", "pvlib/tests/test_modelchain.py::test_infer_dc_model[cec]", "pvlib/tests/test_modelchain.py::test_infer_dc_model[desoto]", "pvlib/tests/test_modelchain.py::test_infer_dc_model[pvsyst]", "pvlib/tests/test_modelchain.py::test_infer_dc_model[singlediode]", "pvlib/tests/test_modelchain.py::test_infer_dc_model[pvwatts_dc]", "pvlib/tests/test_modelchain.py::test_infer_spectral_model[sapm]", "pvlib/tests/test_modelchain.py::test_infer_spectral_model[cec]", "pvlib/tests/test_modelchain.py::test_infer_spectral_model[cec_native]", "pvlib/tests/test_modelchain.py::test_infer_temp_model[sapm_temp]", "pvlib/tests/test_modelchain.py::test_infer_temp_model[faiman_temp]", "pvlib/tests/test_modelchain.py::test_infer_temp_model[pvsyst_temp]", "pvlib/tests/test_modelchain.py::test_infer_temp_model[fuentes_temp]", "pvlib/tests/test_modelchain.py::test_infer_temp_model_invalid", "pvlib/tests/test_modelchain.py::test_infer_temp_model_no_params", "pvlib/tests/test_modelchain.py::test_temperature_model_inconsistent", "pvlib/tests/test_modelchain.py::test_dc_model_user_func", "pvlib/tests/test_modelchain.py::test_ac_models[sandia]", "pvlib/tests/test_modelchain.py::test_ac_models[adr]", "pvlib/tests/test_modelchain.py::test_ac_models[pvwatts]", "pvlib/tests/test_modelchain.py::test_ac_models_deprecated[snlinverter]", "pvlib/tests/test_modelchain.py::test_ac_models_deprecated[adrinverter]", "pvlib/tests/test_modelchain.py::test_ac_model_user_func", "pvlib/tests/test_modelchain.py::test_ac_model_not_a_model", "pvlib/tests/test_modelchain.py::test_aoi_models[sapm]", "pvlib/tests/test_modelchain.py::test_aoi_models[ashrae]", "pvlib/tests/test_modelchain.py::test_aoi_models[physical]", "pvlib/tests/test_modelchain.py::test_aoi_models[martin_ruiz]", "pvlib/tests/test_modelchain.py::test_aoi_model_no_loss", "pvlib/tests/test_modelchain.py::test_aoi_model_user_func", "pvlib/tests/test_modelchain.py::test_infer_aoi_model[sapm]", "pvlib/tests/test_modelchain.py::test_infer_aoi_model[ashrae]", "pvlib/tests/test_modelchain.py::test_infer_aoi_model[physical]", "pvlib/tests/test_modelchain.py::test_infer_aoi_model[martin_ruiz]", "pvlib/tests/test_modelchain.py::test_infer_aoi_model_invalid", "pvlib/tests/test_modelchain.py::test_spectral_models[sapm]", "pvlib/tests/test_modelchain.py::test_spectral_models[first_solar]", "pvlib/tests/test_modelchain.py::test_spectral_models[no_loss]", "pvlib/tests/test_modelchain.py::test_spectral_models[constant_spectral_loss]", "pvlib/tests/test_modelchain.py::test_losses_models_pvwatts", "pvlib/tests/test_modelchain.py::test_losses_models_ext_def", "pvlib/tests/test_modelchain.py::test_losses_models_no_loss", "pvlib/tests/test_modelchain.py::test_invalid_dc_model_params", "pvlib/tests/test_modelchain.py::test_invalid_models[dc_model]", "pvlib/tests/test_modelchain.py::test_invalid_models[ac_model]", "pvlib/tests/test_modelchain.py::test_invalid_models[aoi_model]", "pvlib/tests/test_modelchain.py::test_invalid_models[spectral_model]", "pvlib/tests/test_modelchain.py::test_invalid_models[temperature_model]", "pvlib/tests/test_modelchain.py::test_invalid_models[losses_model]", "pvlib/tests/test_modelchain.py::test_bad_get_orientation", "pvlib/tests/test_modelchain.py::test_deprecated_09[snlinverter]", "pvlib/tests/test_modelchain.py::test_deprecated_09[adrinverter]", "pvlib/tests/test_modelchain.py::test_ModelChain_kwargs_deprecated_09", "pvlib/tests/test_modelchain.py::test_basic_chain_required", "pvlib/tests/test_modelchain.py::test_basic_chain_alt_az", "pvlib/tests/test_modelchain.py::test_basic_chain_strategy", "pvlib/tests/test_modelchain.py::test_basic_chain_altitude_pressure", "pvlib/tests/test_modelchain.py::test_ModelChain___repr__[south_at_latitude_tilt-south_at_latitude_tilt]", "pvlib/tests/test_modelchain.py::test_ModelChain___repr__[None-None]", "pvlib/tests/test_modelchain.py::test_complete_irradiance_clean_run", "pvlib/tests/test_modelchain.py::test_complete_irradiance"]

## 提示信息



---

*此文件由SWE-bench数据自动生成*
*生成时间: 2025-10-20 11:39:41*
