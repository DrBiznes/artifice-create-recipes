package dev.jam.artificecreaterecipes.tests;

import java.util.*;
import java.util.function.Consumer;
import com.simibubi.create.AllRecipeTypes;
import com.simibubi.create.content.processing.recipe.ProcessingRecipe;
import com.simibubi.create.content.processing.sequenced.SequencedAssemblyRecipe;
import dev.jam.artificecreaterecipes.IncompleteItem;
import dev.jam.artificecreaterecipes.WorkpieceNames;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTestGenerator;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.gametest.framework.TestFunction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.*;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.gametest.GameTestHolder;

/** Runs with a real server recipe manager, loaded tags, and Create serializers.
 * Uses native sequence selection/advancement, not a reimplementation of progress.
 * Test mod and structure are excluded from the release jar.
 */
@Mod(FactoryTests.MOD)
@GameTestHolder(FactoryTests.MOD)
public final class FactoryTests {
    public static final String MOD = "artifice_create_recipes_tests";
    private static final String ADDON = "artifice_create_recipes";
    private static final String HEXEREI = "hazens_archaic_hexerei_armaments";

    @GameTestGenerator
    public static Collection<TestFunction> tests() {
        return List.of(test("replacements_and_hats", FactoryTests::replacements),
                test("every_sequence_completes", FactoryTests::sequences),
                test("agreed_material_costs", FactoryTests::costs),
                test("workpieces_and_unlocks", FactoryTests::workpieces),
                test("optional_hexerei_support", FactoryTests::hexerei));
    }

    private static TestFunction test(String name, Consumer<GameTestHelper> body) {
        return new TestFunction("factory", MOD + ":" + name, MOD + ":empty", 100, 0L, true, body);
    }

    private static ResourceLocation id(String name) {
        return ResourceLocation.parse(name.contains(":") ? name : "irons_artifice:" + name);
    }

    private static boolean hexereiLoaded() {
        return ModList.get().isLoaded(HEXEREI);
    }

    private static boolean isAddonNamespace(ResourceLocation id) {
        return id.getNamespace().equals("irons_artifice") || id.getNamespace().equals(HEXEREI);
    }

    private static Recipe<?> recipe(GameTestHelper h, String name) {
        return h.getLevel().getRecipeManager().byKey(id(name)).orElseThrow().value();
    }

    private static void replacements(GameTestHelper h) {
        Map<String, Integer> counts = new HashMap<>();
        for (var holder : h.getLevel().getRecipeManager().getRecipes()) {
            if (!holder.id().getNamespace().equals("irons_artifice")) continue;
            var r = holder.value();
            counts.merge(BuiltInRegistries.RECIPE_TYPE.getKey(r.getType()).toString(), 1, Integer::sum);
            if (r instanceof CraftingRecipe) {
                h.assertTrue(Set.of("cowboy_hat", "tricorne").contains(holder.id().getPath()), "No old crafting bypass: " + holder.id());
            }
            h.assertTrue(!r.getResultItem(h.getLevel().registryAccess()).isEmpty(), "Output resolves: " + holder.id());
            for (var ingredient : r.getIngredients()) {
                h.assertTrue(ingredient.getItems().length > 0, "Ingredient/tag resolves: " + holder.id());
            }
        }
        h.assertTrue(counts.equals(Map.of("create:sequenced_assembly", 23, "create:mixing", 10,
                "create:compacting", 11, "minecraft:crafting", 2)), "All 46 recipes loaded with replacement types: " + counts);
        h.assertTrue(recipe(h, "cowboy_hat") instanceof ShapedRecipe && recipe(h, "tricorne") instanceof ShapedRecipe, "Hats stay craftable");
        h.succeed();
    }

    @SuppressWarnings({"rawtypes", "unchecked"})
    private static void sequences(GameTestHelper h) {
        var level = h.getLevel();
        int completed = 0;
        for (var holder : level.getRecipeManager().getRecipes()) {
            if (!isAddonNamespace(holder.id()) || !(holder.value() instanceof SequencedAssemblyRecipe assembly)) continue;
            var initial = assembly.getIngredient().getItems();
            h.assertTrue(initial.length > 0, "Starter tag resolves: " + holder.id());
            ItemStack current = initial[0].copyWithCount(1);
            int length = assembly.getSequence().size();
            int total = length * assembly.getLoops();
            for (int i = 0; i < total; i++) {
                ProcessingRecipe expected = assembly.getSequence().get(i % length).getRecipe();
                ItemStack held = expected.getIngredients().size() > 1
                        ? ((Ingredient) expected.getIngredients().get(1)).getItems()[0] : ItemStack.EMPTY;
                // The held ingredient distinguishes recipes sharing a starter,
                // matching Create's deployer search behavior.
                var matches = SequencedAssemblyRecipe.getRecipes(level, current, (RecipeType) expected.getType(),
                        (Class) expected.getClass(), candidate -> {
                            ProcessingRecipe r = (ProcessingRecipe) ((RecipeHolder) candidate).value();
                            return held.isEmpty() || ((Ingredient) r.getIngredients().get(1)).test(held);
                        });
                h.assertTrue(matches.size() == 1, "Unambiguous native step " + i + " of " + holder.id() + ": " + matches.size());
                RecipeHolder selected = (RecipeHolder) matches.getFirst();
                h.assertTrue(selected.id().equals(holder.id()), "Correct route selected: " + holder.id());
                ProcessingRecipe step = (ProcessingRecipe) selected.value();
                List<ItemStack> results = step.rollResults(level.random);
                h.assertTrue(results.size() == 1, "Single guaranteed result: " + holder.id());
                current = results.getFirst();
                if (i < total - 1) {
                    h.assertTrue(current.getItem() instanceof IncompleteItem && current.getCount() == 1,
                            "Only a single inert workpiece before completion: " + holder.id());
                }
            }
            ItemStack result = assembly.getResultItem(level.registryAccess());
            h.assertTrue(ItemStack.isSameItemSameComponents(current, result) && current.getCount() == result.getCount(),
                    "Correct completed product/count: " + holder.id());
            h.assertTrue(!(current.getItem() instanceof IncompleteItem), "Workpiece becomes real product");
            completed++;
        }
        int expected = 23 + (hexereiLoaded() ? WorkpieceNames.HEXEREI.size() : 0);
        h.assertTrue(completed == expected, "All " + expected + " sequences completed, got " + completed);
        h.succeed();
    }

    private static int consumed(SequencedAssemblyRecipe r, String item) {
        var stack = BuiltInRegistries.ITEM.get(ResourceLocation.parse(item)).getDefaultInstance();
        int count = r.getIngredient().test(stack) ? 1 : 0;
        for (var s : r.getSequence()) {
            var step = s.getRecipe();
            if (step.getType() == AllRecipeTypes.DEPLOYING.getType()
                    && step.getIngredients().get(1).test(stack)) count += r.getLoops();
        }
        return count;
    }

    private static void cost(GameTestHelper h, String recipe, String item, int expected) {
        int actual = consumed((SequencedAssemblyRecipe) recipe(h, recipe), item);
        h.assertTrue(actual == expected, recipe + " consumes " + expected + " " + item + ", got " + actual);
    }

    private static void costs(GameTestHelper h) {
        cost(h, "bullet_from_iron", "irons_artifice:blackpowder", 24);
        cost(h, "bullet_from_iron", "create:iron_sheet", 1);
        cost(h, "bullet_from_copper", "irons_artifice:blackpowder", 6);
        cost(h, "bullet_from_copper", "create:copper_sheet", 1);
        h.assertTrue(recipe(h, "bullet_from_iron").getResultItem(h.getLevel().registryAccess()).getCount() == 24, "24 iron bullets");
        h.assertTrue(recipe(h, "bullet_from_copper").getResultItem(h.getLevel().registryAccess()).getCount() == 6, "6 copper bullets");
        for (String gun : List.of("flintlock", "blackpowder_revolver", "six_shooter")) cost(h, gun, "minecraft:oak_log", 2);
        for (String gun : List.of("musket", "blunderbuss", "arquebus", "clockwork_rifle")) cost(h, gun, "minecraft:oak_log", 3);
        cost(h, "clockwork_rifle", "minecraft:netherite_scrap", 3);
        cost(h, "simple_mechanical_components", "create:copper_sheet", 1);
        cost(h, "simple_mechanical_components", "create:andesite_alloy", 2);
        cost(h, "mechanical_components", "irons_artifice:simple_mechanical_components", 1);
        cost(h, "mechanical_components", "create:iron_sheet", 4);
        cost(h, "mechanical_components", "minecraft:redstone", 2);
        cost(h, "clockwork_components", "irons_artifice:mechanical_components", 2);
        cost(h, "clockwork_components", "create:precision_mechanism", 1);
        var bayonet = (SequencedAssemblyRecipe) recipe(h, "bayonet_attachment_modifier");
        h.assertTrue(bayonet.getIngredient().test(Items.IRON_SWORD.getDefaultInstance()), "Sword is consumed as base, not damaged as tool");
        var oil = (SequencedAssemblyRecipe) recipe(h, "gun_oil_modifier");
        var fill = oil.getSequence().getLast().getRecipe();
        h.assertTrue(fill.getType() == AllRecipeTypes.FILLING.getType() && fill.getFluidIngredients().getFirst().amount() == 250,
                "Oil requires 250 mB fluid filling");
        h.succeed();
    }

    private static void workpieces(GameTestHelper h) {
        h.assertTrue(WorkpieceNames.ALL.size() == 23, "23 dedicated workpieces");
        for (String name : WorkpieceNames.ALL) {
            var item = BuiltInRegistries.ITEM.get(ResourceLocation.fromNamespaceAndPath(ADDON, name));
            h.assertTrue(item instanceof IncompleteItem, "Registered inert workpiece: " + name);
        }
        for (String name : WorkpieceNames.HEXEREI) {
            boolean registered = BuiltInRegistries.ITEM.containsKey(ResourceLocation.fromNamespaceAndPath(ADDON, name));
            h.assertTrue(registered == hexereiLoaded(), "Hexerei workpiece registered only with Hexerei: " + name);
        }
        for (var r : h.getLevel().getRecipeManager().getRecipes()) {
            if (r.id().getNamespace().equals("irons_artifice") && !(r.value() instanceof CraftingRecipe)) {
                var oldUnlock = id("irons_artifice:recipes/misc/" + r.id().getPath());
                h.assertTrue(h.getLevel().getServer().getAdvancements().get(oldUnlock) == null, "No stale crafting unlock: " + oldUnlock);
            }
        }
        h.assertTrue(h.getLevel().getServer().getAdvancements().get(id("irons_artifice:recipes/misc/cowboy_hat")) != null,
                "Hat recipe advancement retained");
        h.succeed();
    }

    /** Without Hexerei every conditional override must stay out of the recipe manager. */
    private static void hexerei(GameTestHelper h) {
        var recipes = h.getLevel().getRecipeManager().getRecipes();
        if (!hexereiLoaded()) {
            for (var holder : recipes) {
                h.assertTrue(!holder.id().getNamespace().equals(HEXEREI), "Hexerei recipe leaked without Hexerei: " + holder.id());
            }
            h.succeed();
            return;
        }
        for (var holder : recipes) {
            if (holder.id().getNamespace().equals(HEXEREI) && holder.value() instanceof CraftingRecipe) {
                h.assertTrue(!holder.id().getPath().startsWith("crafting/guns/") && !holder.id().getPath().equals("crafting/materials/warhog_cog"),
                        "No crafting-table bypass for Hexerei guns: " + holder.id());
            }
        }
        String cog = HEXEREI + ":crafting/materials/warhog_cog";
        h.assertTrue(recipe(h, cog).getResultItem(h.getLevel().registryAccess()).getCount() == 2, "Cog recipe yields 2");
        cost(h, cog, "irons_artifice:clockwork_components", 2);
        cost(h, cog, "hazentouvelib:steel_block", 2);
        cost(h, cog, "minecraft:netherite_ingot", 1);
        cost(h, HEXEREI + ":crafting/guns/star_cannon", HEXEREI + ":warhog_cog", 2);
        cost(h, HEXEREI + ":crafting/guns/star_cannon", "irons_artifice:clockwork_rifle", 1);
        cost(h, HEXEREI + ":crafting/guns/super_star_shooter", HEXEREI + ":warhog_cog", 2);
        cost(h, HEXEREI + ":crafting/guns/super_star_shooter", HEXEREI + ":star_cannon", 1);
        cost(h, HEXEREI + ":crafting/guns/tactical_crossgun", HEXEREI + ":warhog_cog", 1);
        cost(h, HEXEREI + ":crafting/guns/tactical_crossgun", "irons_spellbooks:mithril_scrap", 2);
        cost(h, HEXEREI + ":crafting/guns/royaltys_barrel", "irons_artifice:blunderbuss", 1);
        cost(h, HEXEREI + ":crafting/guns/royaltys_barrel", "minecraft:quartz", 2);
        h.succeed();
    }
}
