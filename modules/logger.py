#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة نظام السجلات (Logging)
Argan Smart Generator
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional


class AppLogger:
    """نظام السجلات للتطبيق"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern - نسخة واحدة فقط"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """إعداد نظام السجلات"""
        # إنشاء مجلد logs إذا لم يكن موجوداً
        os.makedirs('logs', exist_ok=True)
        
        # إنشاء logger
        self._logger = logging.getLogger('argan_app')
        self._logger.setLevel(logging.INFO)
        
        # تجنب تكرار handlers
        if self._logger.handlers:
            return
        
        # Handler للملف (يحفظ آخر 5 MB، 3 ملفات احتياطية)
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        # Handler للأخطاء (ملف منفصل)
        error_handler = RotatingFileHandler(
            'logs/errors.log',
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        # تنسيق السجلات
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        
        # إضافة handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(error_handler)
    
    def info(self, message: str, user: Optional[str] = None):
        """تسجيل معلومة"""
        if user:
            message = f"[{user}] {message}"
        self._logger.info(message)
    
    def warning(self, message: str, user: Optional[str] = None):
        """تسجيل تحذير"""
        if user:
            message = f"[{user}] {message}"
        self._logger.warning(message)
    
    def error(self, message: str, user: Optional[str] = None, exc_info: bool = False):
        """تسجيل خطأ"""
        if user:
            message = f"[{user}] {message}"
        self._logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str, user: Optional[str] = None):
        """تسجيل معلومات تصحيح"""
        if user:
            message = f"[{user}] {message}"
        self._logger.debug(message)
    
    def log_login(self, username: str, success: bool = True):
        """تسجيل محاولة تسجيل دخول"""
        if success:
            self.info(f"تسجيل دخول ناجح", user=username)
        else:
            self.warning(f"محاولة تسجيل دخول فاشلة", user=username)
    
    def log_logout(self, username: str):
        """تسجيل خروج"""
        self.info(f"تسجيل خروج", user=username)
    
    def log_action(self, action: str, username: str, details: str = ""):
        """تسجيل إجراء"""
        message = f"{action}"
        if details:
            message += f" - {details}"
        self.info(message, user=username)
    
    def log_error_with_context(self, error: Exception, context: str, username: Optional[str] = None):
        """تسجيل خطأ مع السياق"""
        message = f"{context}: {str(error)}"
        self.error(message, user=username, exc_info=True)
    
    def log_api_call(self, api_name: str, username: str, success: bool = True):
        """تسجيل استدعاء API"""
        if success:
            self.info(f"API call successful: {api_name}", user=username)
        else:
            self.error(f"API call failed: {api_name}", user=username)
    
    def log_file_operation(self, operation: str, filename: str, username: str, success: bool = True):
        """تسجيل عملية على ملف"""
        if success:
            self.info(f"File {operation}: {filename}", user=username)
        else:
            self.error(f"File {operation} failed: {filename}", user=username)
    
    def log_database_operation(self, operation: str, table: str, username: str, success: bool = True):
        """تسجيل عملية على قاعدة البيانات"""
        if success:
            self.info(f"Database {operation} on {table}", user=username)
        else:
            self.error(f"Database {operation} failed on {table}", user=username)


# إنشاء نسخة واحدة من Logger
logger = AppLogger()


# دوال مساعدة للاستخدام السريع
def log_info(message: str, user: Optional[str] = None):
    """تسجيل معلومة"""
    logger.info(message, user)


def log_warning(message: str, user: Optional[str] = None):
    """تسجيل تحذير"""
    logger.warning(message, user)


def log_error(message: str, user: Optional[str] = None, exc_info: bool = False):
    """تسجيل خطأ"""
    logger.error(message, user, exc_info)


def log_debug(message: str, user: Optional[str] = None):
    """تسجيل معلومات تصحيح"""
    logger.debug(message, user)


# دوال لقراءة السجلات
def get_recent_logs(lines: int = 100, log_type: str = 'app') -> str:
    """
    قراءة آخر سجلات
    
    Args:
        lines: عدد الأسطر
        log_type: نوع السجل ('app' أو 'errors')
    
    Returns:
        محتوى السجلات
    """
    log_file = f'logs/{log_type}.log'
    
    if not os.path.exists(log_file):
        return "لا توجد سجلات بعد"
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:]
            return ''.join(recent)
    except Exception as e:
        return f"خطأ في قراءة السجلات: {e}"


def get_logs_by_user(username: str, lines: int = 100) -> str:
    """
    قراءة سجلات مستخدم معين
    
    Args:
        username: اسم المستخدم
        lines: عدد الأسطر
    
    Returns:
        سجلات المستخدم
    """
    log_file = 'logs/app.log'
    
    if not os.path.exists(log_file):
        return "لا توجد سجلات بعد"
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            user_lines = [line for line in all_lines if f'[{username}]' in line]
            recent = user_lines[-lines:]
            return ''.join(recent)
    except Exception as e:
        return f"خطأ في قراءة السجلات: {e}"


def get_error_count_today() -> int:
    """الحصول على عدد الأخطاء اليوم"""
    log_file = 'logs/errors.log'
    
    if not os.path.exists(log_file):
        return 0
    
    today = datetime.now().strftime('%Y-%m-%d')
    count = 0
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if today in line and 'ERROR' in line:
                    count += 1
    except:
        pass
    
    return count


def clear_old_logs(days: int = 30):
    """
    حذف السجلات القديمة
    
    Args:
        days: عدد الأيام للاحتفاظ بالسجلات
    """
    # هذه الوظيفة يمكن تطويرها لاحقاً
    # حالياً RotatingFileHandler يتعامل مع هذا تلقائياً
    pass

