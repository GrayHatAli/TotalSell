using Microsoft.Extensions.DependencyInjection;

namespace TotalSell.Application.Mappers;

public static class MapperConfiguration
{
    public static IServiceCollection AddApplicationMappers(this IServiceCollection services)
    {
        var config = new AutoMapper.MapperConfiguration(mc =>
        {
            mc.AddProfile(new CustomerMapperProfile());
            mc.AddProfile(new SupplierMapperProfile());
            mc.AddProfile(new ProductMapperProfile());
            mc.AddProfile(new InvoiceMapperProfile());
            mc.AddProfile(new ReportMapperProfile());
        });

        var mapper = config.CreateMapper();
        services.AddSingleton(mapper);

        return services;
    }
} 