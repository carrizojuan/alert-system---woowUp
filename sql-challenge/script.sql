SELECT 
    CONCAT(c.Nombre, ' ', c.Apellido) AS NombreCompleto, 
    SUM(v.Importe) AS TotalCompras
FROM 
    Clientes c
INNER JOIN 
    Ventas v 
ON 
    c.ID = v.Id_cliente
WHERE 
    v.Fecha >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY 
    c.ID
HAVING 
    SUM(v.Importe) > 100000;