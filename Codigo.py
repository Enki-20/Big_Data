Operaciones principales:
Consultas:
Selección de documentos: Consultar los hurtos ocurridos en un rango de fechas específico (por ejemplo, entre 2018 y 2024).
javascript
Copiar código
db.Capital.find({
  "DEPARTAMENTO": "BOGOTA D.C.",
  "FECHA HECHO": { $gte: ISODate("2018-01-01T00:00:00Z"), $lte: ISODate("2024-12-31T23:59:59Z") }
});
Filtrar y agrupar por municipio: Contar los hurtos por municipio en Bogotá D.C. para ver cuál tiene más casos reportados.
javascript
Copiar código
db.Capital.aggregate([
  { $match: { "DEPARTAMENTO": "BOGOTA D.C." } },
  { $group: { _id: "$MUNICIPIO", total: { $sum: 1 } } },
  { $sort: { total: -1 } }
]);
Promediar hurtos por año: Promediar la cantidad de hurtos por año para ver las tendencias a lo largo del tiempo.
javascript
Copiar código
db.Capital.aggregate([
  { $match: { "DEPARTAMENTO": "BOGOTA D.C." } },
  { $group: { _id: { $year: "$FECHA HECHO" }, avgCantidad: { $avg: "$CANTIDAD" } } },
  { $sort: { avgCantidad: -1 } }
]);
 Estrategias de indexación:
En MongoDB, para mejorar el rendimiento de las consultas, puedes crear índices en los campos que más se consultan, como DEPARTAMENTO, FECHA HECHO, y MUNICIPIO.
Ejemplo para crear un índice compuesto en DEPARTAMENTO y FECHA HECHO:
javascript
Copiar código
db.Capital.createIndex({ "DEPARTAMENTO": 1, "FECHA HECHO": 1 });
Este índice permitirá realizar consultas más rápidas cuando se filtren los documentos por DEPARTAMENTO y FECHA HECHO.
Manejo de datos:
Inserción de documentos:
Para insertar un nuevo documento (hurto de vivienda), se puede usar el siguiente comando:
javascript
Copiar código
db.Capital.insertOne({
  "FECHA HECHO": ISODate("2024-11-01T00:00:00Z"),
  "COD_DEPTO": 11,
  "DEPARTAMENTO": "BOGOTA D.C.",
  "COD_MUNI": 11001,
  "MUNICIPIO": "BOGOTA, D.C.",
  "CANTIDAD": 5
});
Actualización de documentos:
Para actualizar la cantidad de hurtos en un documento específico:
javascript
Copiar código
db.Capital.updateOne(
  { "MUNICIPIO": "BOGOTA, D.C.", "FECHA HECHO": ISODate("2024-11-01T00:00:00Z") },
  { $set: { "CANTIDAD": 10 } }
);
Eliminación de documentos:
Para eliminar documentos con fechas anteriores a 2010:
javascript
Copiar código
db.Capital.deleteMany({ "FECHA HECHO": { $lt: ISODate("2010-01-01T00:00:00Z") } });
