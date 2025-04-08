using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TotalSell.Application.Common.Persistence;
using TotalSell.Infrastructure.Persistence;

namespace TotalSell.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<TotalSell.Infrastructure.Persistence.ApplicationDbContext>(options =>
            options.UseNpgsql(configuration.GetConnectionString("DefaultConnection")));

        services.AddScoped<IApplicationDbContext>(provider => provider.GetRequiredService<TotalSell.Infrastructure.Persistence.ApplicationDbContext>());

        return services;
    }
} 