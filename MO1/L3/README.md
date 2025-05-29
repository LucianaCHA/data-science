# Análisis SQL Avanzado - PaperGalaxy S.A.

Este repositorio contiene el análisis solicitado por Mariana Ruiz, jefa del equipo de datos de PaperGalaxy S.A., en base a la base de datos `sales_office.db`.

## 📁 Estructura del proyecto


---

## ✅ Consultas realizadas

### 1. Productos con precio mayor al promedio general

**Consulta utilizada:**

```sql
SELECT * FROM sales
WHERE priceeach > (
    SELECT AVG(priceeach) FROM sales
);
```
**Resultado:**

