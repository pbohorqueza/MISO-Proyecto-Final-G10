package com.example.ccpapplication.navigation.graph

import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.rememberNavController
import com.example.ccpapplication.AppViewModel
import com.example.ccpapplication.services.interceptors.TokenManager

object Graph {
    const val AUTHENTICATION = "auth_graph"
    const val CLIENT = "client_graph"
    const val ADMIN="admin_graph"
    const val SCHEDULE_VISIT = "schedule_visit"
    const val CLIENTS = "clients"
    const val VISITS = "visits"
    const val VENDEDOR_SHOPPING="vendedor_shopping"
}

@Composable
fun AppNavGraph(navController: NavHostController = rememberNavController(),
                appViewModel: AppViewModel, modifier: Modifier,tokenManager:TokenManager) {
    NavHost(
        navController = navController,
        route = "root",
        startDestination = Graph.AUTHENTICATION ,
        modifier = modifier
    ) {
        authNavGraph(navController = navController,appViewModel = appViewModel)
        clientNavGraph(navController = navController,tokenManager=tokenManager)
        mainNavGraph(navController = navController,tokenManager=tokenManager)
    }
}