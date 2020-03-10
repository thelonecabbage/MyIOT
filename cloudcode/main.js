Parse.Cloud.define("deviceUpdate", async (request) => {
  // return request.params
  const query = new Parse.Query("Device");
  query.equalTo("objectId", request.params.objectId);
  const device = await query.first({useMasterKey:true});
  let settings, telemetry
  if (device) {
    settings = {
      ...device.get('settings'),
      ...(request.params.settings || {})
    }

    telemetry = {
      ...device.get('telemetry'),
      ...(request.params.telemetry || {})
    }
    device.set('settings', settings)
    device.set('telemetry', telemetry)
    device.save(null, {useMasterKey: true})
    return device.toJSON()
  }
  throw new Parse.Error(404, 'Device not found');
});
/**

curl -X POST \
 -H "X-Parse-Application-Id: l6HsMGQ3ugnZcQOkiH1wG7Iy6IRKhx7RDvqQp8Vz" \
 -H "X-Parse-REST-API-Key: 5wRkTx5Yd1rmVcq6J6iTTcBDSNulN3f7Z2x7AgcR" \
 -H "Content-Type: application/json" \
 -d "{\"objectId\": \"TEwQLdzSkI\", \"settings\": {}, \"telemetry\": {\"grill\": 120}}" \
  https://grillporn.back4app.io/functions/deviceUpdate

 */

