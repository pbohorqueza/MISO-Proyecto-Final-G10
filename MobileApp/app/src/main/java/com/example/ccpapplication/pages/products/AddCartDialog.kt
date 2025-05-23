package com.example.ccpapplication.pages.products

import androidx.compose.foundation.layout.Column
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import com.example.ccpapplication.data.model.Producto

@Composable
fun AddToCartDialog(
    product: Producto,
    maxQuantity: Int,
    onDismiss: () -> Unit,
    onAdd: (cantidad: Int) -> Boolean // <- Ahora devuelve un booleano
) {
    var quantityText by remember { mutableStateOf("") }
    var error by remember { mutableStateOf(false) }
    var stockError by remember { mutableStateOf(false) }

    AlertDialog(
        onDismissRequest = { onDismiss() },
        title = { Text(text = "Agregar al carrito") },
        text = {
            Column {
                Text("Ingrese la cantidad (máx: $maxQuantity)")
                OutlinedTextField(
                    value = quantityText,
                    onValueChange = {
                        if (it.all { char -> char.isDigit() }) quantityText = it
                        error = false
                        stockError = false
                    },
                    isError = error || stockError,
                    label = { Text("Cantidad") },
                    singleLine = true
                )
                if (error) {
                    Text("Cantidad inválida", color = MaterialTheme.colorScheme.error)
                }
                if (stockError) {
                    Text("No hay suficiente stock disponible", color = MaterialTheme.colorScheme.error)
                }
            }
        },
        confirmButton = {
            TextButton(onClick = {
                val cantidad = quantityText.toIntOrNull()
                if (cantidad == null || cantidad <= 0 || cantidad > maxQuantity) {
                    error = true
                } else {
                    val success = onAdd(cantidad)
                    if (success) {
                        onDismiss()
                    } else {
                        stockError = true
                    }
                }
            }) {
                Text("Agregar")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancelar")
            }
        }
    )
}

