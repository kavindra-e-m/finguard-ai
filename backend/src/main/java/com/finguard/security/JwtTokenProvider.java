package com.finguard.security;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT Token provider for authentication.
 */
@Slf4j
@Component
public class JwtTokenProvider {
    
    @Value("${jwt.secret}")
    private String jwtSecret;
    
    @Value("${jwt.expiration}")
    private long jwtExpiration;
    
    /**
     * Generate JWT token from authentication.
     *
     * @param authentication the authentication object
     * @return JWT token string
     */
    public String generateToken(Authentication authentication) {
        UserPrincipal userPrincipal = (UserPrincipal) authentication.getPrincipal();
        Date expiryDate = new Date(System.currentTimeMillis() + jwtExpiration);
        
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
        
        return Jwts.builder()
                .setSubject(Long.toString(userPrincipal.getId()))
                .claim("email", userPrincipal.getEmail())
                .claim("name", userPrincipal.getName())
                .setIssuedAt(new Date())
                .setExpiration(expiryDate)
                .signWith(key, SignatureAlgorithm.HS512)
                .compact();
    }
    
    /**
     * Generate token directly from user details.
     *
     * @param userId the user ID
     * @param email the user email
     * @param name the user name
     * @return JWT token string
     */
    public String generateToken(Long userId, String email, String name) {
        Date expiryDate = new Date(System.currentTimeMillis() + jwtExpiration);
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
        
        return Jwts.builder()
                .setSubject(Long.toString(userId))
                .claim("email", email)
                .claim("name", name)
                .setIssuedAt(new Date())
                .setExpiration(expiryDate)
                .signWith(key, SignatureAlgorithm.HS512)
                .compact();
    }
    
    /**
     * Get user ID from token.
     *
     * @param token the JWT token
     * @return user ID
     */
    public Long getUserIdFromToken(String token) {
        Claims claims = parseToken(token);
        return Long.parseLong(claims.getSubject());
    }
    
    /**
     * Validate JWT token.
     *
     * @param token the JWT token
     * @return true if valid
     */
    public boolean validateToken(String token) {
        try {
            parseToken(token);
            return true;
        } catch (ExpiredJwtException e) {
            log.error("JWT token is expired: {}", e.getMessage());
        } catch (UnsupportedJwtException e) {
            log.error("JWT token is unsupported: {}", e.getMessage());
        } catch (MalformedJwtException e) {
            log.error("JWT token is malformed: {}", e.getMessage());
        } catch (SignatureException e) {
            log.error("JWT signature validation failed: {}", e.getMessage());
        } catch (IllegalArgumentException e) {
            log.error("JWT token is empty or null: {}", e.getMessage());
        }
        return false;
    }
    
    /**
     * Parse JWT token and return claims.
     *
     * @param token the JWT token
     * @return claims
     */
    private Claims parseToken(String token) {
        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
        
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}
