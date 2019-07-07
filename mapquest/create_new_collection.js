
db.incidents_mapquest_sc.find({}).forEach(function(x){

    var y = new Object();

    y.type = "Point";
    y.coordinates = [x.lng, x.lat];
    x.location = y;

    db.incidents_mapquest_st.replaceOne({_id : x._id}, x, {upsert: true});

});

db.incidents_mapquest_st.createIndex( {location : "2dsphere" } );