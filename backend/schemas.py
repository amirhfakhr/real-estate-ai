from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
import re


class SearchRequest(BaseModel):

    # -----------------------------
    # اطلاعات کاربر
    # -----------------------------

    name: str = Field(
        min_length=2,
        max_length=100
    )

    phone: str

    # -----------------------------
    # موقعیت
    # -----------------------------

    province: str = Field(
        min_length=2,
        max_length=50
    )

    city: str = Field(
        min_length=2,
        max_length=50
    )

    area_name: Optional[str] = Field(
        default=None,
        max_length=100
    )

    # -----------------------------
    # هدف و نوع ملک
    # -----------------------------

    purpose: str

    property_type: str

    # -----------------------------
    # متراژ
    # -----------------------------

    min_area: Optional[float] = Field(
        default=None,
        ge=0
    )

    max_area: Optional[float] = Field(
        default=None,
        ge=0
    )

    # -----------------------------
    # بودجه
    # -----------------------------

    min_budget: Optional[float] = Field(
        default=None,
        ge=0
    )

    max_budget: Optional[float] = Field(
        default=None,
        ge=0
    )

    # -----------------------------
    # نیازها
    # -----------------------------

    requirements: list[str] = Field(
        default_factory=list
    )


    # ==================================================
    # PHONE VALIDATION
    # ==================================================

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:

        # حذف فاصله و خط تیره
        value = value.strip().replace(" ", "").replace("-", "")

        # فرمت موبایل ایران
        pattern = r"^(?:\+98|0098|98|0)9\d{9}$"

        if not re.fullmatch(pattern, value):
            raise ValueError(
                "شماره موبایل معتبر ایران وارد کنید."
            )

        # تبدیل همه حالت‌ها به فرمت استاندارد
        if value.startswith("+98"):
            value = "0" + value[3:]

        elif value.startswith("0098"):
            value = "0" + value[4:]

        elif value.startswith("98"):
            value = "0" + value[2:]

        return value


    # ==================================================
    # STRING CLEANING
    # ==================================================

    @field_validator(
        "name",
        "province",
        "city",
        "area_name"
    )
    @classmethod
    def clean_strings(cls, value):

        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


    # ==================================================
    # PURPOSE
    # ==================================================

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, value):

        allowed = {
            "living",
            "investment",
            "rental"
        }

        if value not in allowed:
            raise ValueError(
                "هدف خرید نامعتبر است."
            )

        return value


    # ==================================================
    # PROPERTY TYPE
    # ==================================================

    @field_validator("property_type")
    @classmethod
    def validate_property_type(cls, value):

        allowed = {
            "apartment",
            "villa"
        }

        if value not in allowed:
            raise ValueError(
                "نوع ملک نامعتبر است."
            )

        return value


    # ==================================================
    # REQUIREMENTS
    # ==================================================

    @field_validator("requirements")
    @classmethod
    def validate_requirements(cls, value):

        cleaned = []

        for item in value:

            item = item.strip()

            if item:
                cleaned.append(item)

        # جلوگیری از تعداد غیرمنطقی
        if len(cleaned) > 20:
            raise ValueError(
                "تعداد امکانات درخواستی بیش از حد مجاز است."
            )

        return cleaned


    # ==================================================
    # RANGE VALIDATION
    # ==================================================

    @model_validator(mode="after")
    def validate_ranges(self):

        # متراژ
        if (
            self.min_area is not None
            and self.max_area is not None
            and self.min_area > self.max_area
        ):
            raise ValueError(
                "حداقل متراژ نمی‌تواند بیشتر از حداکثر متراژ باشد."
            )

        # بودجه
        if (
            self.min_budget is not None
            and self.max_budget is not None
            and self.min_budget > self.max_budget
        ):
            raise ValueError(
                "حداقل بودجه نمی‌تواند بیشتر از حداکثر بودجه باشد."
            )

        return self