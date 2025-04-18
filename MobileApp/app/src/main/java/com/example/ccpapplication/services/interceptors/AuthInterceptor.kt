package com.example.ccpapplication.services.interceptors

import okhttp3.Interceptor
import okhttp3.Response

// services/interceptors/AuthInterceptor.kt
class AuthInterceptor(private val tokenManager: TokenManager) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()

        // Evitar agregar token a la ruta de login
        if (originalRequest.url.encodedPath.contains("/auth")) {
            return chain.proceed(originalRequest)
        }

        val requestWithAuth = originalRequest.newBuilder()
        tokenManager.getToken()?.let { token ->
            requestWithAuth.addHeader("Authorization", "Bearer $token")
        }

        return chain.proceed(requestWithAuth.build())
    }
}