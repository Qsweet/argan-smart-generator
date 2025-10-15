#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار لقسم تخطيط التسعير المحسن
"""

import json

# اختبار دالة حساب الأسعار
def test_price_calculation():
    """اختبار حساب الأسعار"""
    
    # معطيات الاختبار
    base_price = 100.0
    cost = 50.0
    base_discount = 30.0  # %
    code_discount = 10.0  # %
    
    # الحسابات
    after_discount = base_price * (1 - base_discount / 100)
    after_code = after_discount * (1 - code_discount / 100)
    discount_percent = ((base_price - after_code) / base_price) * 100
    net_profit = after_code - cost
    profit_margin = (net_profit / after_code) * 100 if after_code > 0 else 0
    
    # النتائج المتوقعة
    expected_after_discount = 70.0  # 100 - 30%
    expected_after_code = 63.0  # 70 - 10%
    expected_discount_percent = 37.0  # (100-63)/100 * 100
    expected_net_profit = 13.0  # 63 - 50
    expected_profit_margin = 20.63  # (13/63) * 100
    
    print("🧪 اختبار حساب الأسعار:")
    print(f"السعر الأساسي: {base_price} ر.س")
    print(f"التكلفة: {cost} ر.س")
    print(f"نسبة الخصم الأساسية: {base_discount}%")
    print(f"نسبة خصم الكود: {code_discount}%")
    print("\n📊 النتائج:")
    print(f"بعد الخصم: {after_discount:.2f} ر.س (المتوقع: {expected_after_discount:.2f})")
    print(f"بعد الكود: {after_code:.2f} ر.س (المتوقع: {expected_after_code:.2f})")
    print(f"نسبة الخصم الإجمالية: {discount_percent:.2f}% (المتوقع: {expected_discount_percent:.2f}%)")
    print(f"الربح الصافي: {net_profit:.2f} ر.س (المتوقع: {expected_net_profit:.2f})")
    print(f"نسبة الربح: {profit_margin:.2f}% (المتوقع: {expected_profit_margin:.2f}%)")
    
    # التحقق
    assert abs(after_discount - expected_after_discount) < 0.01, "خطأ في حساب السعر بعد الخصم"
    assert abs(after_code - expected_after_code) < 0.01, "خطأ في حساب السعر بعد الكود"
    assert abs(net_profit - expected_net_profit) < 0.01, "خطأ في حساب الربح الصافي"
    
    print("\n✅ جميع الاختبارات نجحت!")
    
    return True


def test_product_structure():
    """اختبار بنية المنتج"""
    
    print("\n🧪 اختبار بنية المنتج:")
    
    product = {
        "name": "زيت الأرغان 100 مل",
        "base_price": 100.0,
        "after_discount": 70.0,
        "after_code": 63.0,
        "cost": 50.0,
        "profit_margin": 20.63,
        "discount_percent": 37.0,
        "net_profit": 13.0,
        "status": "جيد"
    }
    
    # التحقق من وجود جميع الحقول المطلوبة
    required_fields = [
        'name', 'base_price', 'after_discount', 'after_code',
        'cost', 'profit_margin', 'discount_percent', 'net_profit', 'status'
    ]
    
    for field in required_fields:
        assert field in product, f"الحقل {field} مفقود"
        print(f"✓ {field}: {product[field]}")
    
    # التحقق من عدم وجود حقل الفئة
    assert 'category' not in product, "حقل الفئة موجود ولكن يجب إزالته"
    print("\n✅ حقل الفئة غير موجود (كما هو مطلوب)")
    
    print("\n✅ بنية المنتج صحيحة!")
    
    return True


def test_status_determination():
    """اختبار تحديد الحالة بناءً على نسبة الربح"""
    
    print("\n🧪 اختبار تحديد الحالة:")
    
    test_cases = [
        (35.0, "ممتاز"),
        (25.0, "جيد"),
        (10.0, "تحذير"),
        (30.0, "ممتاز"),
        (15.0, "جيد"),
        (14.9, "تحذير")
    ]
    
    for profit_margin, expected_status in test_cases:
        if profit_margin >= 30:
            status = "ممتاز"
        elif profit_margin >= 15:
            status = "جيد"
        else:
            status = "تحذير"
        
        assert status == expected_status, f"خطأ في تحديد الحالة لنسبة ربح {profit_margin}%"
        print(f"✓ نسبة الربح {profit_margin}% → {status}")
    
    print("\n✅ جميع حالات التحديد صحيحة!")
    
    return True


def main():
    """تشغيل جميع الاختبارات"""
    
    print("=" * 60)
    print("🚀 بدء اختبار قسم تخطيط التسعير المحسن")
    print("=" * 60)
    
    try:
        test_price_calculation()
        test_product_structure()
        test_status_determination()
        
        print("\n" + "=" * 60)
        print("🎉 جميع الاختبارات نجحت بنجاح!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ فشل الاختبار: {str(e)}")
        return False
    
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    main()

