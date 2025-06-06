package com.example.ccpapplication.pages.register

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelProvider.AndroidViewModelFactory.Companion.APPLICATION_KEY
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.example.ccpapplication.App
import com.example.ccpapplication.R
import com.example.ccpapplication.data.repository.UserRepository
import com.example.ccpapplication.data.model.User
import com.example.ccpapplication.data.model.UserRegistration
import kotlinx.coroutines.launch

class RegisterViewModel(protected val errorMessages: ValidationErrorMessages,
                        private val userRepository: UserRepository
) : ViewModel() {
    // Declaración de textos usados en la app
    var firstName by mutableStateOf("")
    var lastName by mutableStateOf("")
    var email by mutableStateOf("")
    var password by mutableStateOf("")
    var confirmPassword by mutableStateOf("")
    var clientType by mutableStateOf("TENDERO") // Valor TENDERO por defecto
    
    var firstNameError by mutableStateOf<String?>(null)
    var lastNameError by mutableStateOf<String?>(null)
    var emailError by mutableStateOf<String?>(null)
    var passwordError by mutableStateOf<String?>(null)
    var confirmPasswordError by mutableStateOf<String?>(null)
    
    var isLoading by mutableStateOf(false)
    var registrationSuccessful by mutableStateOf(false)
    var errorMessage by mutableStateOf<String?>(null)




    // Función para validar los campos de entrada del formulario
    open fun validateInputs(): Boolean {
        var isValid = true
        
        // Validar nombre
        if (firstName.isBlank()) {
            firstNameError = errorMessages.firstNameEmpty
            isValid = false
        } else {
            firstNameError = null
        }
        
        // Validar apellido
        if (lastName.isBlank()) {
            lastNameError = errorMessages.lastNameEmpty
            isValid = false
        } else {
            lastNameError = null
        }
        
        // Validar email
        if (email.isBlank()) {
            emailError = errorMessages.emailEmpty
            isValid = false
        } else {
            // Usar una expresión regular simple cuando estamos en entorno de pruebas (Patterns.EMAIL_ADDRESS es nulo)
            val isValidEmail = try {
                android.util.Patterns.EMAIL_ADDRESS?.matcher(email)?.matches() ?: 
                    Regex("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}$").matches(email)
            } catch (e: Exception) {
                // Fallback para pruebas unitarias
                Regex("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}$").matches(email)
            }
            
            if (!isValidEmail) {
                emailError = errorMessages.emailInvalid
                isValid = false
            } else {
                emailError = null
            }
        }
        
        // Validar contraseña
        if (password.isBlank()) {
            passwordError = errorMessages.passwordEmpty
            isValid = false
        } else if (password.length < 8) {
            passwordError = errorMessages.passwordLength
            isValid = false
        } else {
            passwordError = null
        }
        
        // Validar confirmación de contraseña
        if (confirmPassword.isBlank()) {
            confirmPasswordError = errorMessages.confirmPasswordEmpty
            isValid = false
        } else if (confirmPassword != password) {
            confirmPasswordError = errorMessages.passwordMismatch
            isValid = false
        } else {
            confirmPasswordError = null
        }
        
        return isValid
    }


    fun register(onComplete: (Boolean) -> Unit) {
        if (validateInputs()) {
            viewModelScope.launch {
                isLoading = true

                val user = UserRegistration(
                    username = email,
                    password = password,
                    firstname = firstName,
                    lastname = lastName,
                    rol = clientType
                )

                val result = userRepository.registerUser(user)

                result.fold(
                    onSuccess = { response ->
                        isLoading = false
                        registrationSuccessful = true
                        onComplete(true)
                    },
                    onFailure = { exception ->
                        isLoading = false
                        errorMessage = exception.message
                        onComplete(false)
                    }
                )
            }
        } else {
            onComplete(false)
        }
    }
    
    fun resetForm() {
        firstName = ""
        lastName = ""
        email = ""
        password = ""
        confirmPassword = ""
        clientType = "TENDERO"
        firstNameError = null
        lastNameError = null
        emailError = null
        passwordError = null
        confirmPasswordError = null
        isLoading = false
        registrationSuccessful = false
        errorMessage = null
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val application = (this[APPLICATION_KEY] as App)
                val userRepository = application.container.userRepository
                val errorMessages = ValidationErrorMessages(
                    firstNameEmpty = application.getString(R.string.register_validation_error_firstname_empty),
                    lastNameEmpty = application.getString(R.string.register_validation_error_lastname_empty),
                    emailEmpty = application.getString(R.string.register_validation_error_email_empty),
                    emailInvalid = application.getString(R.string.register_validation_error_email_invalid),
                    passwordEmpty = application.getString(R.string.register_validation_error_password_empty),
                    passwordLength = application.getString(R.string.register_validation_error_pwd_length),
                    confirmPasswordEmpty = application.getString(R.string.register_validation_error_password_empty),
                    passwordMismatch = application.getString(R.string.register_validation_error_pwd_mismatch)
                )
                RegisterViewModel(errorMessages = errorMessages,userRepository = userRepository)
            }
        }
    }
}

// Clase para encapsular todos los mensajes de error de validación
data class ValidationErrorMessages(
    val firstNameEmpty: String,
    val lastNameEmpty: String,
    val emailEmpty: String,
    val emailInvalid: String,
    val passwordEmpty: String,
    val passwordLength: String,
    val confirmPasswordEmpty: String,
    val passwordMismatch: String
)