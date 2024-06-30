db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "users",
      required: ["_id", "userid"],
      properties: {
        "_id": { bsonType: "objectId" },
        "name": { bsonType: "object", title: "name", properties: { "first": { bsonType: "string" }, "last": { bsonType: "string" }, }, },
        "email": { bsonType: "string" },
        "userid": { bsonType: "string" },
        "creation-date": { bsonType: "date" },
        "modification-date": { bsonType: "date" },
      },
    },
  },
});

db.createCollection("plates", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "plates",
      required: ["_id", "plate-number"],
      properties: {
        "_id": { bsonType: "objectId" },
        "plate-number": { bsonType: "string" },
        "modifications": { bsonType: "array", items: { bsonType: "object" } },
        "locations": { bsonType: "array", items: { bsonType: "object" } },
        "images": { bsonType: "array", items: { bsonType: "objectId" } },
        "creation-date": { bsonType: "date" },
      },
    },
  },
});

db.createCollection("samples", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "samples",
      required: ["_id", "sample-number"],
      properties: {
        "_id": { bsonType: "objectId" },
        "sample-number": { bsonType: "int" },
        "owners": { bsonType: "array", items: { bsonType: "object" } },
        "information": { bsonType: "object", title: "information", properties: { "origin": { bsonType: "objectId" }, "material": { bsonType: "string" }, "orientation": { bsonType: "string" }, "doping": { bsonType: "string" }, "growth": { bsonType: "string" }, "note": { bsonType: "string" }, "damaged": { bsonType: "object", title: "damaged", properties: { "date": { bsonType: "date" }, "note": { bsonType: "string" }, }, }, "lost": { bsonType: "object", title: "lost", properties: { "date": { bsonType: "date" }, "note": { bsonType: "string" }, }, }, }, },
        "locations": { bsonType: "array", items: { bsonType: "object" } },
        "images": { bsonType: "array", items: { bsonType: "objectId" } },
        "files": { bsonType: "array", items: { bsonType: "objectId" } },
        "creation-date": { bsonType: "date" },
      },
    },
  },
});

db.createCollection("fs.chunks", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "fs.chunks",
      required: ["_id"],
      properties: {
        "_id": { bsonType: "objectId" },
        "files_id": { bsonType: "objectId" },
        "n": { bsonType: "int" },
        "data": { bsonType: "binData" },
      },
    },
  },
});

db.createCollection("fs.files", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "fs.files",
      required: ["_id"],
      properties: {
        "_id": { bsonType: "objectId" },
        "length": { bsonType: "int" },
        "chunkSize": { bsonType: "int" },
        "uploadDate": { bsonType: "date" },
        "md5": { bsonType: "string" },
        "filename": { bsonType: "string" },
        "contentType": { bsonType: "string" },
        "aliases": { bsonType: "array", items: { bsonType: "string" } },
        "metadata": { bsonType: "any" },
      },
    },
  },
});

db.createCollection("new-plates", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "new-plates",
      required: ["_id"],
      properties: {
        "_id": { bsonType: "objectId" },
        "plate_id": { bsonType: "objectId" },
        "plate-number": { bsonType: "int" },
        "creation-date": { bsonType: "date" },
      },
    },
  },
});

db.createCollection("new-users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "new-users",
      required: ["_id"],
      properties: {
        "_id": { bsonType: "objectId" },
        "user_id": { bsonType: "objectId" },
        "uuid": { bsonType: "string" },
        "creation-date": { bsonType: "date" },
      },
    },
  },
});

db.createCollection("new-samples", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "new-samples",
      required: ["_id"],
      properties: {
        "_id": { bsonType: "objectId" },
        "sample_id": { bsonType: "objectId" },
        "sample-number": { bsonType: "int" },
        "material": { bsonType: "string" },
        "orientation": { bsonType: "string" },
        "origin": { bsonType: "string" },
        "creation-date": { bsonType: "date" },
      },
    },
  },
});

db.createCollection("locations", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      title: "locations",
      required: ["_id"],
      properties: {
        "_id": { bsonType: "objectId" },
        "name": { bsonType: "string" },
        "location": { bsonType: "object", title: "location", properties: { "address": { bsonType: "object", title: "address", properties: { "street": { bsonType: "string" }, "zip": { bsonType: "string" }, "city": { bsonType: "string" }, "country": { bsonType: "string" }, }, }, "room": { bsonType: "string" }, }, },
        "creation-date": { bsonType: "date" },
        "modification-date": { bsonType: "date" },
      },
    },
  },
});