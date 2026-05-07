package com.finguard;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.servers.Server;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Main entry point for FinGuard AI Backend Application.
 */
@SpringBootApplication
@OpenAPIDefinition(
        info = @Info(
                title = "FinGuard AI API",
                version = "1.0.0",
                description = "REST API for FinGuard AI - Intelligent Financial Assistance Platform"
        ),
        servers = @Server(url = "/", description = "Default Server")
)
public class FinGuardApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(FinGuardApplication.class, args);
    }
}
