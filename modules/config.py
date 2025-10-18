#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة إدارة الإعدادات والمتغيرات البيئية
Argan Smart Generator - Configuration Module
"""

import os
from dotenv import load_dotenv
from typing import Optional


# تحميل المتغيرات البيئية من ملف .env
load_dotenv()


class Config:
    """إدارة إعدادات التطبيق"""
    
    # =============================================================================
    # OpenAI Configuration
    # =============================================================================
    
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_MAX_TOKENS: int = int(os.getenv('OPENAI_MAX_TOKENS', '1500'))
    OPENAI_TEMPERATURE: float = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # =============================================================================
    # Database Configuration
    # =============================================================================
    
    DATABASE_PATH: str = os.getenv('DATABASE_PATH', 'database/')
    CUSTOMERS_DB: str = os.getenv('CUSTOMERS_DB', 'customers.db')
    REVENUES_DB: str = os.getenv('REVENUES_DB', 'revenues.db')
    
    @classmethod
    def get_customers_db_path(cls) -> str:
        """الحصول على المسار الكامل لقاعدة بيانات العملاء"""
        return os.path.join(cls.DATABASE_PATH, cls.CUSTOMERS_DB)
    
    @classmethod
    def get_revenues_db_path(cls) -> str:
        """الحصول على المسار الكامل لقاعدة بيانات الإيرادات"""
        return os.path.join(cls.DATABASE_PATH, cls.REVENUES_DB)
    
    # =============================================================================
    # Security Configuration
    # =============================================================================
    
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'default-secret-key-change-this')
    SESSION_TIMEOUT: int = int(os.getenv('SESSION_TIMEOUT', '3600'))
    MAX_LOGIN_ATTEMPTS: int = int(os.getenv('MAX_LOGIN_ATTEMPTS', '5'))
    BLOCK_DURATION: int = int(os.getenv('BLOCK_DURATION', '900'))
    
    # =============================================================================
    # Application Configuration
    # =============================================================================
    
    APP_NAME: str = os.getenv('APP_NAME', 'Argan Smart Generator')
    APP_VERSION: str = os.getenv('APP_VERSION', '7.4')
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
    
    # =============================================================================
    # Logging Configuration
    # =============================================================================
    
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_SIZE: int = int(os.getenv('LOG_MAX_SIZE', '5242880'))  # 5 MB
    LOG_BACKUP_COUNT: int = int(os.getenv('LOG_BACKUP_COUNT', '5'))
    
    # =============================================================================
    # Rate Limiting
    # =============================================================================
    
    RATE_LIMIT_ENABLED: bool = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60'))
    
    # =============================================================================
    # Backup Configuration
    # =============================================================================
    
    BACKUP_DIR: str = os.getenv('BACKUP_DIR', 'backups/')
    BACKUP_RETENTION_DAYS: int = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
    AUTO_BACKUP_ENABLED: bool = os.getenv('AUTO_BACKUP_ENABLED', 'True').lower() == 'true'
    
    # =============================================================================
    # Validation Methods
    # =============================================================================
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """التحقق من صحة الإعدادات"""
        errors = []
        
        # التحقق من OpenAI API Key
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == 'your_openai_api_key_here':
            errors.append("⚠️ OPENAI_API_KEY غير محدد أو غير صحيح")
        
        # التحقق من SECRET_KEY
        if cls.SECRET_KEY == 'default-secret-key-change-this':
            errors.append("⚠️ SECRET_KEY يجب تغييره من القيمة الافتراضية")
        
        # التحقق من وجود المجلدات
        if not os.path.exists(cls.DATABASE_PATH):
            errors.append(f"⚠️ مجلد قاعدة البيانات غير موجود: {cls.DATABASE_PATH}")
        
        if not os.path.exists(cls.BACKUP_DIR):
            errors.append(f"⚠️ مجلد النسخ الاحتياطية غير موجود: {cls.BACKUP_DIR}")
        
        if not os.path.exists('logs'):
            errors.append("⚠️ مجلد السجلات غير موجود: logs/")
        
        return len(errors) == 0, errors
    
    @classmethod
    def print_config(cls):
        """طباعة الإعدادات الحالية (بدون المعلومات الحساسة)"""
        print("=" * 60)
        print(f"⚙️  إعدادات {cls.APP_NAME} v{cls.APP_VERSION}")
        print("=" * 60)
        
        print(f"\n🤖 OpenAI:")
        print(f"   Model: {cls.OPENAI_MODEL}")
        print(f"   Max Tokens: {cls.OPENAI_MAX_TOKENS}")
        print(f"   Temperature: {cls.OPENAI_TEMPERATURE}")
        print(f"   API Key: {'✅ محدد' if cls.OPENAI_API_KEY else '❌ غير محدد'}")
        
        print(f"\n💾 Database:")
        print(f"   Path: {cls.DATABASE_PATH}")
        print(f"   Customers DB: {cls.CUSTOMERS_DB}")
        print(f"   Revenues DB: {cls.REVENUES_DB}")
        
        print(f"\n🔒 Security:")
        print(f"   Max Login Attempts: {cls.MAX_LOGIN_ATTEMPTS}")
        print(f"   Block Duration: {cls.BLOCK_DURATION}s")
        print(f"   Session Timeout: {cls.SESSION_TIMEOUT}s")
        
        print(f"\n📝 Logging:")
        print(f"   Level: {cls.LOG_LEVEL}")
        print(f"   File: {cls.LOG_FILE}")
        print(f"   Max Size: {cls.LOG_MAX_SIZE / 1024 / 1024:.1f} MB")
        
        print(f"\n🔄 Backup:")
        print(f"   Directory: {cls.BACKUP_DIR}")
        print(f"   Retention: {cls.BACKUP_RETENTION_DAYS} days")
        print(f"   Auto Backup: {'✅' if cls.AUTO_BACKUP_ENABLED else '❌'}")
        
        print(f"\n🐛 Debug Mode: {'✅' if cls.DEBUG_MODE else '❌'}")
        
        print(f"\n" + "=" * 60)
        
        # التحقق من الإعدادات
        is_valid, errors = cls.validate()
        
        if is_valid:
            print("✅ جميع الإعدادات صحيحة")
        else:
            print("⚠️  تحذيرات:")
            for error in errors:
                print(f"   {error}")
        
        print("=" * 60)


# إنشاء instance عام
config = Config()


# =============================================================================
# Helper Functions
# =============================================================================

def get_openai_api_key() -> str:
    """الحصول على OpenAI API Key"""
    return config.OPENAI_API_KEY


def is_debug_mode() -> bool:
    """التحقق من وضع التصحيح"""
    return config.DEBUG_MODE


def get_database_path(db_name: str) -> str:
    """الحصول على المسار الكامل لقاعدة بيانات"""
    return os.path.join(config.DATABASE_PATH, db_name)


# =============================================================================
# Main - للاختبار
# =============================================================================

if __name__ == '__main__':
    config.print_config()

