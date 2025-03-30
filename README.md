# TotalSell

سیستم مدیریت فروش و خرید با قابلیت‌های پیشرفته

## ویژگی‌ها

- مدیریت مشتریان
- مدیریت تامین‌کنندگان
- مدیریت محصولات و دسته‌بندی‌ها
- مدیریت فاکتورها و پیش‌فاکتورها
- مدیریت حساب‌های بانکی
- سیستم گزارش‌گیری پیشرفته

## تکنولوژی‌ها

- .NET 8
- Clean Architecture
- Domain-Driven Design
- Docker
- Entity Framework Core
- MediatR
- AutoMapper
- FluentValidation
- Serilog
- Swagger

## پیش‌نیازها

- .NET 8 SDK
- Docker Desktop
- Visual Studio 2022 یا VS Code

## نحوه اجرا

1. کلون کردن پروژه
2. اجرای دستور `dotnet restore`
3. اجرای دستور `docker-compose up -d`
4. اجرای پروژه

## ساختار پروژه

```
TotalSell/
├── src/
│   ├── Core/
│   │   ├── TotalSell.Domain/
│   │   ├── TotalSell.Application/
│   │   └── TotalSell.Shared/
│   ├── Infrastructure/
│   │   ├── TotalSell.Infrastructure/
│   │   └── TotalSell.Persistence/
│   └── Presentation/
│       ├── TotalSell.API/
│       └── TotalSell.Report.API/
└── tests/
```

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. 